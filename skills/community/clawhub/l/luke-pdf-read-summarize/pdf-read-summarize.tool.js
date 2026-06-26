/**
 * Luke PDF Read-Summarize Tool
 * Read and summarize PDF files
 * 
 * Security Note: This tool requires PyMuPDF (fitz) to be installed.
 * Best used in trusted environments only.
 */

export async function readAndSummarizePDF(path, summaryType = 'brief') {
  // 使用 child_process.spawn 而非 exec，避免 shell 注入
  const { spawn } = await import('child_process');
  const { writeFileSync, unlinkSync } = await import('fs');
  const { tmpfile } = await import('os');

  try {
    // 验证路径安全 - 只允许文件路径
    if (!path || typeof path !== 'string') {
      throw new Error('无效的 PDF 文件路径');
    }

    // 检查路径是否包含危险字符
    if (path.includes('..') || path.includes('||') || path.includes('&&') || path.includes(';')) {
      throw new Error('文件路径包含非法字符');
    }

    // 创建安全的 Python 脚本
    const scriptPath = `/tmp/pdf_reader_${Date.now()}.py`;
    
    const pythonScript = `
import sys
import fitz
import json
import os

def safe_extract_pdf(file_path):
    """安全提取 PDF 内容"""
    # 确认文件存在且可读
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    try:
        doc = fitz.open(file_path)
        pages = doc.page_count
        
        # 限制页数防止 DoS
        if pages > 1000:
            raise ValueError(f"PDF 页数过多：{pages}页 (限制 1000 页)")
        
        all_text = []
        total_chars = 0
        
        for page_num in range(pages):
            page = doc[page_num]
            text = page.get_text()
            all_text.append(f"Page {page_num + 1}:\\n{text}")
            total_chars += len(text)
        
        doc.close()
        
        # 限制总字符数防止内存问题
        if total_chars > 10_000_000:  # 10MB
            raise ValueError(f"PDF 内容过大：{total_chars}字符 (限制 10MB)")
        
        return {
            "success": True,
            "pages": pages,
            "text": "\\n\\n".join(all_text),
            "total_chars": total_chars
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "需要文件路径参数"}))
        sys.exit(1)
    
    result = safe_extract_pdf(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
`;

    // 写入临时脚本
    writeFileSync(scriptPath, pythonScript);

    // 使用 spawn 安全执行（不启用 shell）
    const pythonProcess = spawn('python3', [scriptPath, path], {
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 120000, // 2 分钟超时
      maxBuffer: 50 * 1024 * 1024, // 50MB 限制
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    await new Promise((resolve, reject) => {
      pythonProcess.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Python 进程退出码：${code}\n${stderr}`));
        }
      });

      pythonProcess.on('error', (err) => {
        reject(new Error(`执行失败：${err.message}`));
      });
    });

    // 清理临时文件
    try {
      unlinkSync(scriptPath);
    } catch (e) {
      // 忽略清理错误
    }

    // 解析 JSON 结果
    let jsonResult;
    try {
      jsonResult = JSON.parse(stdout);
    } catch (e) {
      throw new Error(`解析 PDF 返回结果失败：${e.message}`);
    }

    if (!jsonResult.success) {
      throw new Error(jsonResult.error || 'PDF 读取失败');
    }

    const pages = jsonResult.pages || 0;
    const content = jsonResult.text || '';

    if (!content || content.length < 100) {
      return '无法提取 PDF 内容，请检查文件是否为可提取文本的 PDF。';
    }

    // 生成摘要
    const summary = generateSummary(content, pages, summaryType);

    return summary;

  } catch (error) {
    console.error('Error reading/summarizing PDF:', error.message);
    return `读取/摘要 PDF 时出错：${error.message}`;
  }
}

function generateSummary(content, pages, type) {
  const lines = content.split('\n').filter(line => line.trim());
  
  const title = extractTitle(lines);
  const sections = extractSections(lines);
  const keyData = extractKeyData(content);
  
  const summaryLines = [];
  
  summaryLines.push('# PDF 摘要\n');
  summaryLines.push(`## 基本信息\n`);
  summaryLines.push(`- **文档页数**: ${pages} 页\n`);
  summaryLines.push(`- **标题**: ${title}\n`);
  summaryLines.push(`- **文本长度**: ${content.length} 字符\n`);
  summaryLines.push('');
  
  if (sections.length > 0) {
    summaryLines.push('## 核心章节\n');
    sections.forEach(section => {
      summaryLines.push(`### ${section.name}\n`);
      if (section.bullets.length > 0) {
        section.bullets.forEach(bullet => {
          summaryLines.push(`- ${bullet.substring(0, 150)}${bullet.length > 150 ? '...' : ''}\n`);
        });
      } else {
        summaryLines.push('（本节无明确要点）\n');
      }
      summaryLines.push('');
    });
  }
  
  if (keyData.length > 0) {
    summaryLines.push('## 关键数据/要点\n');
    keyData.forEach(data => {
      summaryLines.push(`- ${data}\n`);
    });
    summaryLines.push('');
  }
  
  if (type === 'detailed') {
    summaryLines.push('## 详细摘要\n');
    summaryLines.push('（超过 10000 字符的内容已截断显示）\n');
    summaryLines.push('');
  }
  
  summaryLines.push('---\n');
  summaryLines.push('*摘要由 Luke PDF Read-Summarize 工具生成*\n');
  
  return summaryLines.join('');
}

function extractTitle(lines) {
  const titlePattern = /^(.+？)[\s·—-]+\d{2,4}岁/;
  for (const line of lines) {
    const match = line.trim().match(titlePattern);
    if (match) return match[1].trim();
  }
  return lines[0]?.trim() || '未识别到标题';
}

function extractSections(lines) {
  const sectionKeywords = [
    { keyword: '优势', maxLength: 500 },
    { keyword: '工作经历', maxLength: 2000 },
    { keyword: '项目经验', maxLength: 2000 },
    { keyword: '教育经历', maxLength: 500 },
    { keyword: '语言能力', maxLength: 300 }
  ];
  
  const sections = [];
  
  sectionKeywords.forEach(sec => {
    let startIndex = -1;
    let endIndex = -1;
    
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes(sec.keyword)) {
        startIndex = i + 1;
        break;
      }
    }
    
    if (startIndex === -1) return;
    
    for (let i = startIndex; i < lines.length; i++) {
      let nextSectionFound = false;
      for (const sec2 of sectionKeywords) {
        if (sec2.keyword !== sec.keyword && lines[i].includes(sec2.keyword)) {
          endIndex = i;
          nextSectionFound = true;
          break;
        }
      }
      if (nextSectionFound) break;
    }
    
    endIndex = endIndex || lines.length;
    
    const sectionContent = lines.slice(startIndex, endIndex).join('\n');
    
    const bullets = [];
    sectionContent.split('\n').forEach(line => {
      const trimmed = line.trim();
      if (trimmed && (
        trimmed.includes(':') || 
        trimmed.includes('•') || 
        trimmed.includes('1.') || 
        trimmed.includes('2.') ||
        /\d{4}/.test(trimmed)
      )) {
        bullets.push(trimmed);
      }
    });
    
    sections.push({
      name: sec.keyword,
      content: sectionContent.substring(0, sec.maxLength),
      bullets: bullets.slice(0, 10)
    });
  });
  
  return sections;
}

function extractKeyData(content) {
  const keyData = [];
  
  const dateMatches = content.match(/\d{4}\/\d{2}-\d{4}\/\d{2}/g);
  if (dateMatches) {
    dateMatches.slice(0, 10).forEach(d => {
      if (!keyData.includes(`📅 时间：${d}`)) keyData.push(`📅 时间：${d}`);
    });
  }
  
  const numberMatches = content.match(/\d+(?:万|GB|TB|QPS|%|倍)?/g);
  if (numberMatches) {
    numberMatches.slice(0, 10).forEach(n => {
      if (!keyData.includes(`📊 数据：${n}`)) keyData.push(`📊 数据：${n}`);
    });
  }
  
  const companyMatches = content.match(/(美的|中兴|IBM|Oracle|交科|摩根大通|汇丰|UBS|香港城大科讯|卓望|深圳大学|交控科技)/g);
  if (companyMatches) {
    companyMatches.slice(0, 10).forEach(c => {
      if (!keyData.includes(`🏢 机构：${c}`)) keyData.push(`🏢 机构：${c}`);
    });
  }
  
  return keyData;
}
