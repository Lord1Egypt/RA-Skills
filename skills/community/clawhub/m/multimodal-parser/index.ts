import { z } from "https://deno.land/x/zod@v3.22.4/mod.ts";

// 类型定义
const MultimodalParserParams = z.object({
  file_path: z.string(),
  file_type: z.enum(["image", "pdf", "docx", "audio", "auto"]).optional().default("auto"),
  output_format: z.enum(["text", "markdown", "structured"]).optional().default("text"),
  options: z.object({
    ocr_lang: z.string().optional().default("chi_sim+eng"),
    audio_model: z.string().optional().default("base"),
    extract_images: z.boolean().optional().default(false),
    pdf_page_range: z.tuple([z.number(), z.number()]).optional(),
  }).optional().default({})
});

type MultimodalParserParams = z.infer<typeof MultimodalParserParams>;

/**
 * 检查依赖是否存在
 */
async function checkDependency(cmd: string): Promise<boolean> {
  try {
    const res = await new Deno.Command(cmd, { 
      args: ["--version"],
      stderr: "null",
      stdout: "null"
    }).output();
    return res.success;
  } catch {
    return false;
  }
}

/**
 * 检测文件类型
 */
function detectFileType(filePath: string): string | null {
  const ext = filePath.split(".").pop()?.toLowerCase();
  const typeMap: Record<string, string> = {
    "jpg": "image", "jpeg": "image", "png": "image", "webp": "image", "bmp": "image",
    "pdf": "pdf",
    "docx": "docx", "doc": "docx",
    "mp3": "audio", "wav": "audio", "m4a": "audio", "flac": "audio", "ogg": "audio"
  };
  return ext ? typeMap[ext] || null : null;
}

/**
 * 图片解析（OCR）
 */
async function parseImage(filePath: string, options: any): Promise<any> {
  // 检查依赖
  if (!await checkDependency("tesseract")) {
    throw new Error("OCR依赖未安装，请执行：\n- macOS: brew install tesseract tesseract-lang\n- Ubuntu: apt install tesseract-ocr tesseract-ocr-chi-sim");
  }

  const args = [filePath, "stdout", "-l", options.ocr_lang || "chi_sim+eng"];
  const cmd = new Deno.Command("tesseract", { args });
  const { stdout, stderr, success } = await cmd.output();
  
  if (!success) {
    throw new Error(`OCR失败：${new TextDecoder().decode(stderr)}`);
  }
  
  const text = new TextDecoder().decode(stdout).trim();
  return {
    text,
    metadata: { 
      file_type: "image", 
      ocr_lang: options.ocr_lang,
      file_size: (await Deno.stat(filePath)).size
    }
  };
}

/**
 * PDF解析
 */
async function parsePdf(filePath: string, options: any): Promise<any> {
  if (!await checkDependency("pdftotext")) {
    throw new Error("PDF解析依赖未安装，请执行：\n- macOS: brew install poppler\n- Ubuntu: apt install poppler-utils");
  }

  const args = ["-layout"];
  if (options.pdf_page_range) {
    args.push("-f", options.pdf_page_range[0].toString(), "-l", options.pdf_page_range[1].toString());
  }
  args.push(filePath, "-");

  const cmd = new Deno.Command("pdftotext", { args });
  const { stdout, stderr, success } = await cmd.output();
  
  if (!success) {
    throw new Error(`PDF解析失败：${new TextDecoder().decode(stderr)}`);
  }
  
  const text = new TextDecoder().decode(stdout).trim();
  return {
    text,
    metadata: { 
      file_type: "pdf",
      page_range: options.pdf_page_range,
      file_size: (await Deno.stat(filePath)).size
    }
  };
}

/**
 * Docx解析
 */
async function parseDocx(filePath: string, options: any): Promise<any> {
  if (!await checkDependency("pandoc")) {
    throw new Error("DOCX解析依赖未安装，请执行：\n- macOS: brew install pandoc\n- Ubuntu: apt install pandoc");
  }

  const cmd = new Deno.Command("pandoc", { args: [filePath, "-t", "markdown"] });
  const { stdout, stderr, success } = await cmd.output();
  
  if (!success) {
    throw new Error(`DOCX解析失败：${new TextDecoder().decode(stderr)}`);
  }
  
  const text = new TextDecoder().decode(stdout).trim();
  return {
    text,
    metadata: { 
      file_type: "docx",
      file_size: (await Deno.stat(filePath)).size
    }
  };
}

/**
 * 音频解析（转文字）
 */
async function parseAudio(filePath: string, options: any): Promise<any> {
  if (!await checkDependency("whisper")) {
    throw new Error("音频转文字依赖未安装，请执行：pip install openai-whisper ffmpeg");
  }

  const args = [
    filePath, 
    "--model", options.audio_model || "base", 
    "--output_format", "txt",
    "--output_dir", "-"
  ];

  const cmd = new Deno.Command("whisper", { args });
  const { stdout, stderr, success } = await cmd.output();
  
  if (!success) {
    throw new Error(`音频转文字失败：${new TextDecoder().decode(stderr)}`);
  }
  
  const text = new TextDecoder().decode(stdout).trim();
  return {
    text,
    metadata: { 
      file_type: "audio", 
      model: options.audio_model,
      file_size: (await Deno.stat(filePath)).size
    }
  };
}

/**
 * 转换为Markdown格式
 */
function convertToMarkdown(result: any, fileType: string): string {
  const header = `# ${fileType.toUpperCase()} 解析结果\n\n`;
  const metadata = result.metadata ? `## 元数据\n\`\`\`json\n${JSON.stringify(result.metadata, null, 2)}\n\`\`\`\n\n` : "";
  const content = `## 内容\n\n${result.text}`;
  return header + metadata + content;
}

/**
 * OpenClaw Skill: 多模态内容解析器
 * 统一解析图片、PDF、Word、音频等多格式文件，输出结构化文本
 */
export default async function multimodalParser(params: MultimodalParserParams) {
  const validatedParams = MultimodalParserParams.parse(params);
  const { file_path, file_type, output_format, options } = validatedParams;

  // 检查文件是否存在
  try {
    await Deno.stat(file_path);
  } catch {
    return { success: false, error: `文件不存在：${file_path}` };
  }

  // 自动检测文件类型
  const detectedType = file_type === "auto" 
    ? detectFileType(file_path) 
    : file_type;

  if (!detectedType) {
    return { success: false, error: "不支持的文件类型，支持：jpg/png/pdf/docx/mp3/wav/m4a" };
  }

  try {
    let result: any;

    switch (detectedType) {
      case "image":
        result = await parseImage(file_path, options);
        break;
      case "pdf":
        result = await parsePdf(file_path, options);
        break;
      case "docx":
        result = await parseDocx(file_path, options);
        break;
      case "audio":
        result = await parseAudio(file_path, options);
        break;
      default:
        return { success: false, error: "不支持的文件类型" };
    }

    // 格式化输出
    let output: string | object;
    switch (output_format) {
      case "markdown":
        output = convertToMarkdown(result, detectedType);
        break;
      case "structured":
        output = result;
        break;
      default:
        output = result.text;
    }

    return {
      success: true,
      file_type: detectedType,
      output_format,
      content: output,
      metadata: result.metadata || {}
    };

  } catch (error) {
    return {
      success: false,
      error: `解析失败：${(error as Error).message}`
    };
  }
}
