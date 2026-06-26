#!/usr/bin/env node
/**
 * PPT to Video Generator v2.0 - 纯技术合成脚本
 *
 * 职责：PPT截图 → TTS合成 → 视频拼接 → 质量验证
 * 不做：内容判断、风格检测、讲稿改写、markdown清洗
 *
 * 输入要求：
 *   --slides     <path>   PPT/PDF 文件（必需）
 *   --scripts-dir <path>  纯文本讲稿目录（必需）
 *   --output     <path>   输出目录（必需）
 *   --spec       <path>   方案JSON（可选，含逐页音色/语速配置）
 *   --project-dir <path>  项目目录（可选，临时文件放在此目录下）
 *
 * 用法:
 *   node generate.js \
 *     --slides presentation.pptx \
 *     --scripts-dir scripts_rewritten/ \
 *     --output ./video/ \
 *     --spec video_design_spec.json \
 *     --project-dir ./project/ppt-20260509/
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ========== 参数解析 ==========
function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      let value = true;
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        value = args[i + 1];
        i++;
      }
      result[key] = value;
    }
  }
  return result;
}

// ========== 配置与默认值 ==========
const DEFAULT_VOICE = 'zh-CN-YunxiNeural';
const DEFAULT_RATE = '+15%';

// ========== 阶段 1: PPT 截图 ==========
function screenshotSlides(pptPath, outputDir) {
  console.log('\n=== 阶段 1: PPT 截图 ===');
  fs.mkdirSync(outputDir, { recursive: true });

  const screenshots = [];

  if (pptPath.endsWith('.pptx') || pptPath.endsWith('.ppt')) {
    try {
      // LibreOffice 转 PDF
      console.log('  → LibreOffice 转换 PDF...');
      execSync(
        `libreoffice --headless --convert-to pdf --outdir "${outputDir}" "${pptPath}"`,
        { timeout: 120000, stdio: 'pipe' }
      );

      const pdfFile = fs.readdirSync(outputDir).find(f => f.endsWith('.pdf') && !f.startsWith('temp_'));
      if (!pdfFile) {
        throw new Error('PDF 文件未生成');
      }
      const pdfPath = path.join(outputDir, pdfFile);

      // pdftoppm 导出 PNG
      console.log('  → pdftoppm 导出 PNG...');
      execSync(
        `pdftoppm -png -r 150 "${pdfPath}" "${outputDir}/slide"`,
        { timeout: 120000, stdio: 'pipe' }
      );

      // 清理 PDF
      try { fs.unlinkSync(pdfPath); } catch (e) { /* ignore */ }

      // 重命名
      const pngFiles = fs.readdirSync(outputDir)
        .filter(f => f.startsWith('slide-') && f.endsWith('.png'))
        .sort();

      pngFiles.forEach((png, i) => {
        const oldPath = path.join(outputDir, png);
        const newPath = path.join(outputDir, `${String(i + 1).padStart(2, '0')}.png`);
        fs.renameSync(oldPath, newPath);
        screenshots.push(newPath);
      });

    } catch (e) {
      console.error('  ❌ PPT 截图失败：' + e.message);
      throw e;
    }
  } else if (pptPath.endsWith('.pdf')) {
    try {
      console.log('  → pdftoppm 直接处理 PDF...');
      execSync(
        `pdftoppm -png -r 150 "${pptPath}" "${outputDir}/slide"`,
        { timeout: 120000, stdio: 'pipe' }
      );

      const pngFiles = fs.readdirSync(outputDir)
        .filter(f => f.startsWith('slide-') && f.endsWith('.png'))
        .sort();

      pngFiles.forEach((png, i) => {
        const oldPath = path.join(outputDir, png);
        const newPath = path.join(outputDir, `${String(i + 1).padStart(2, '0')}.png`);
        fs.renameSync(oldPath, newPath);
        screenshots.push(newPath);
      });
    } catch (e) {
      console.error('  ❌ PDF 截图失败：' + e.message);
      throw e;
    }
  } else {
    throw new Error('不支持的文件格式: ' + pptPath);
  }

  console.log(`  ✅ 共 ${screenshots.length} 页截图`);
  return screenshots;
}

// ========== 阶段 2: TTS 语音合成 ==========
function synthesizeTTS(scriptsDir, spec, audioDir) {
  console.log('\n=== 阶段 2: TTS 语音合成 ===');
  fs.mkdirSync(audioDir, { recursive: true });

  // 读取所有 .txt 文件
  const scriptFiles = fs.readdirSync(scriptsDir)
    .filter(f => f.endsWith('.txt'))
    .sort();

  if (scriptFiles.length === 0) {
    throw new Error('讲稿目录为空，未找到 .txt 文件');
  }

  console.log(`  → 找到 ${scriptFiles.length} 页讲稿`);

  const audioFiles = [];

  for (let i = 0; i < scriptFiles.length; i++) {
    const scriptPath = path.join(scriptsDir, scriptFiles[i]);
    const audioFile = path.join(audioDir, `audio_${String(i + 1).padStart(2, '0')}.mp3`);

    // 读取纯文本（无需清洗）
    const scriptText = fs.readFileSync(scriptPath, 'utf-8').trim();

    if (!scriptText) {
      console.log(`  ⚠️  第 ${i + 1} 页讲稿为空，跳过`);
      audioFiles.push(null);
      continue;
    }

    // 从 spec 读取该页配置
    let voice = DEFAULT_VOICE;
    let rate = DEFAULT_RATE;

    if (spec && spec.pages && spec.pages[i]) {
      voice = spec.pages[i].voice || voice;
      rate = spec.pages[i].rate || rate;
    } else if (spec && spec.global) {
      voice = spec.global.defaultVoice || voice;
      rate = spec.global.rate || rate;
    }

    // 文本超长时分段合成
    if (scriptText.length > 3000) {
      console.log(`  → 第 ${i + 1} 页文本较长（${scriptText.length}字），分段合成...`);
      const segments = splitTextForTTS(scriptText);
      const segmentAudios = [];

      for (let j = 0; j < segments.length; j++) {
        const segAudio = path.join(audioDir, `audio_${String(i + 1).padStart(2, '0')}_seg${j}.mp3`);
        try {
          execSync(
            `edge-tts --text "${escapeForShell(segments[j])}" --voice ${voice} --rate ${rate} --write-media "${segAudio}"`,
            { stdio: 'pipe', timeout: 120000 }
          );
          segmentAudios.push(segAudio);
        } catch (e) {
          console.warn(`  ⚠️  第 ${i + 1} 页第 ${j + 1} 段 TTS 失败：${e.message}`);
        }
      }

      // 合并分段
      if (segmentAudios.length > 0) {
        if (segmentAudios.length === 1) {
          fs.renameSync(segmentAudios[0], audioFile);
        } else {
          const fileList = path.join(audioDir, `concat_${String(i + 1).padStart(2, '0')}.txt`);
          fs.writeFileSync(fileList, segmentAudios.map(f => `file '${f}'`).join('\n'));
          execSync(
            `ffmpeg -y -f concat -safe 0 -i "${fileList}" -c copy "${audioFile}"`,
            { stdio: 'pipe' }
          );
          // 清理分段文件
          segmentAudios.forEach(f => { try { fs.unlinkSync(f); } catch (e) {} });
          try { fs.unlinkSync(fileList); } catch (e) {}
        }
      }
    } else {
      // 单次合成
      try {
        execSync(
          `edge-tts --text "${escapeForShell(scriptText)}" --voice ${voice} --rate ${rate} --write-media "${audioFile}"`,
          { stdio: 'pipe', timeout: 120000 }
        );
      } catch (e) {
        console.warn(`  ⚠️  第 ${i + 1} 页 TTS 失败：${e.message}`);
      }
    }

    if (fs.existsSync(audioFile) && fs.statSync(audioFile).size > 0) {
      audioFiles.push(audioFile);
      const sizeKB = Math.round(fs.statSync(audioFile).size / 1024);
      const duration = getAudioDuration(audioFile).toFixed(1);
      console.log(`  ✓ 第 ${i + 1} 页 ${sizeKB}KB ${duration}s`);
    } else {
      audioFiles.push(null);
      console.log(`  ✗ 第 ${i + 1} 页 合成失败`);
    }
  }

  return audioFiles;
}

/**
 * 将长文本分段（按句号分割，每段不超过 2500 字）
 */
function splitTextForTTS(text) {
  const sentences = text.split(/([。！？；\n])/);
  const segments = [];
  let current = '';

  for (let i = 0; i < sentences.length; i++) {
    const part = sentences[i];
    if ((current + part).length > 2500 && current.length > 0) {
      segments.push(current.trim());
      current = '';
    }
    current += part;
  }
  if (current.trim()) segments.push(current.trim());

  return segments;
}

/**
 * Shell 文本转义（双引号内的内容）
 */
function escapeForShell(text) {
  return text
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\$/g, '\\$')
    .replace(/`/g, '\\`');
}

// ========== 阶段 3: 视频合成 ==========
function synthesizeVideo(screenshots, audioFiles, clipsDir, finalVideo) {
  console.log('\n=== 阶段 3: 视频合成 ===');
  fs.mkdirSync(clipsDir, { recursive: true });

  const clipFiles = [];

  for (let i = 0; i < screenshots.length && i < audioFiles.length; i++) {
    const screenshot = screenshots[i];
    const audioFile = audioFiles[i];
    const clipFile = path.join(clipsDir, `clip_${String(i + 1).padStart(2, '0')}.mp4`);

    if (!audioFile) {
      console.log(`  ⚠️  第 ${i + 1} 页无音频，跳过`);
      continue;
    }

    try {
      execSync(
        `ffmpeg -y -loop 1 -i "${screenshot}" -i "${audioFile}" ` +
        `-c:v libx264 -tune stillimage -c:a aac -b:a 128k -pix_fmt yuv420p ` +
        `-vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" ` +
        `-shortest -movflags +faststart "${clipFile}"`,
        { stdio: 'pipe' }
      );

      if (fs.existsSync(clipFile) && fs.statSync(clipFile).size > 0) {
        clipFiles.push(clipFile);
      }
    } catch (e) {
      console.warn(`  ⚠️  第 ${i + 1} 页视频合成失败：${e.message}`);
    }
  }

  if (clipFiles.length === 0) {
    console.error('❌ 无有效视频片段');
    return false;
  }

  console.log(`  → ${clipFiles.length} 个片段，开始拼接...`);

  const fileList = path.join(clipsDir, 'files.txt');
  fs.writeFileSync(fileList, clipFiles.map(c => `file '${c}'`).join('\n'));

  execSync(
    `ffmpeg -y -f concat -safe 0 -i "${fileList}" -c copy -movflags +faststart "${finalVideo}"`,
    { stdio: 'pipe' }
  );

  return true;
}

// ========== 阶段 4: 质量验证 ==========
function verifyVideo(videoPath, expectedPages) {
  console.log('\n=== 阶段 4: 质量验证 ===');

  const report = {
    file: videoPath,
    checks: [],
    passed: true
  };

  // 1. 文件存在
  if (!fs.existsSync(videoPath)) {
    report.checks.push({ item: '文件存在', status: 'FAIL', msg: '文件不存在' });
    report.passed = false;
    return report;
  }

  const size = fs.statSync(videoPath).size;
  const sizeMB = (size / 1048576).toFixed(1);
  if (size < 1048576) {
    report.checks.push({ item: '文件大小', status: 'FAIL', msg: `${sizeMB}MB < 1MB` });
    report.passed = false;
  } else {
    report.checks.push({ item: '文件大小', status: 'PASS', msg: `${sizeMB}MB` });
  }

  // 2. ffprobe 解析
  try {
    const info = JSON.parse(
      execSync(
        `ffprobe -v error -show_entries stream=codec_name,width,height,duration -show_entries format=duration,bit_rate -of json "${videoPath}"`,
        { encoding: 'utf-8' }
      )
    );

    const streams = info.streams || [];
    const videoStream = streams.find(s => s.codec_type === 'video') || streams[0];
    const audioStream = streams.find(s => s.codec_type === 'audio') || streams[1];

    // 编码格式
    if (videoStream && videoStream.codec_name === 'h264') {
      report.checks.push({ item: '视频编码', status: 'PASS', msg: 'H.264' });
    } else {
      report.checks.push({ item: '视频编码', status: 'WARN', msg: videoStream?.codec_name || 'unknown' });
    }

    if (audioStream && audioStream.codec_name === 'aac') {
      report.checks.push({ item: '音频编码', status: 'PASS', msg: 'AAC' });
    } else {
      report.checks.push({ item: '音频编码', status: 'WARN', msg: audioStream?.codec_name || 'unknown' });
    }

    // 分辨率
    const w = videoStream?.width || 0;
    const h = videoStream?.height || 0;
    if (w === 1280 && h === 720) {
      report.checks.push({ item: '分辨率', status: 'PASS', msg: `${w}x${h}` });
    } else {
      report.checks.push({ item: '分辨率', status: 'WARN', msg: `${w}x${h} (期望 1280x720)` });
    }

    // 时长
    const duration = info.format?.duration || videoStream?.duration || 0;
    report.checks.push({ item: '总时长', status: 'INFO', msg: `${parseFloat(duration).toFixed(1)}s` });

  } catch (e) {
    report.checks.push({ item: 'ffprobe 解析', status: 'FAIL', msg: e.message });
    report.passed = false;
  }

  // 3. 页数匹配
  if (expectedPages > 0 && clipFilesCount(clipsDirFor(videoPath)) !== expectedPages) {
    report.checks.push({ item: '页数匹配', status: 'WARN', msg: `期望 ${expectedPages} 页` });
  } else {
    report.checks.push({ item: '页数匹配', status: 'PASS' });
  }

  return report;
}

function clipsDirFor(videoPath) {
  return path.join(path.dirname(videoPath), 'clips');
}

function clipFilesCount(dir) {
  try {
    return fs.readdirSync(dir).filter(f => f.startsWith('clip_') && f.endsWith('.mp4')).length;
  } catch {
    return 0;
  }
}

// ========== 辅助函数 ==========
function getAudioDuration(audioFile) {
  try {
    const output = execSync(
      `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "${audioFile}"`,
      { encoding: 'utf-8' }
    );
    return parseFloat(output.trim());
  } catch {
    return 5.0;
  }
}

function getVideoDuration(videoFile) {
  try {
    const output = execSync(
      `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "${videoFile}"`,
      { encoding: 'utf-8' }
    );
    return parseFloat(output.trim());
  } catch {
    return 0;
  }
}

// ========== 主函数 ==========
async function main() {
  const args = parseArgs(process.argv.slice(2));

  console.log('\n🎬 PPT to Video Generator v2.0');
  console.log('   纯技术合成脚本 — 不做内容决策');

  // ===== 参数验证 =====
  if (!args.slides) {
    console.error('\n❌ 缺少必需参数: --slides <PPT/PDF路径>');
    process.exit(1);
  }
  if (!args['scripts-dir']) {
    console.error('\n❌ 缺少必需参数: --scripts-dir <讲稿目录>');
    process.exit(1);
  }
  if (!args.output) {
    console.error('\n❌ 缺少必需参数: --output <输出目录>');
    process.exit(1);
  }

  const slidesPath = path.resolve(args.slides);
  const scriptsDir = path.resolve(args['scripts-dir']);
  const outputDir = path.resolve(args.output);
  const specPath = args.spec ? path.resolve(args.spec) : null;

  if (!fs.existsSync(slidesPath)) {
    console.error(`\n❌ PPT 文件不存在: ${slidesPath}`);
    process.exit(1);
  }
  if (!fs.existsSync(scriptsDir)) {
    console.error(`\n❌ 讲稿目录不存在: ${scriptsDir}`);
    process.exit(1);
  }

  // 读取方案配置（可选）
  let spec = null;
  if (specPath && fs.existsSync(specPath)) {
    try {
      spec = JSON.parse(fs.readFileSync(specPath, 'utf-8'));
      console.log(`\n📋 加载方案配置: ${spec.global?.styleName || spec.global?.style || 'unknown'}`);
    } catch (e) {
      console.warn(`\n⚠️  方案 JSON 解析失败，使用默认配置: ${e.message}`);
    }
  }

  fs.mkdirSync(outputDir, { recursive: true });

  // 临时目录：优先使用 --project-dir/.temp/，否则用输入文件同级目录的 .ppt_video_temp/
  let tempDir;
  if (args['project-dir']) {
    tempDir = path.resolve(args['project-dir'], '.temp');
    console.log(`📂 项目目录: ${args['project-dir']}`);
  } else {
    tempDir = path.join(path.dirname(slidesPath), '.ppt_video_temp');
  }
  const screenshotsDir = path.join(tempDir, 'screenshots');
  const audioDir = path.join(tempDir, 'audio');
  const clipsDir = path.join(tempDir, 'clips');

  console.log(`\n📁 PPT: ${path.basename(slidesPath)}`);
  console.log(`📝 讲稿: ${scriptsDir}`);
  console.log(`📤 输出: ${outputDir}`);

  // ===== 阶段 1: PPT 截图 =====
  const screenshots = screenshotSlides(slidesPath, screenshotsDir);
  if (screenshots.length === 0) {
    console.error('\n❌ 截图失败');
    process.exit(1);
  }

  // ===== 阶段 2: TTS 合成 =====
  const audioFiles = synthesizeTTS(scriptsDir, spec, audioDir);

  // ===== 阶段 3: 视频合成 =====
  const date = args.date || new Date().toISOString().split('T')[0];
  const finalVideo = path.join(outputDir, `video_${date}.mp4`);
  const success = synthesizeVideo(screenshots, audioFiles, clipsDir, finalVideo);

  if (!success) {
    console.error('\n❌ 视频合成失败');
    process.exit(1);
  }

  // ===== 阶段 4: 质量验证 =====
  const report = verifyVideo(finalVideo, screenshots.length);

  // ===== 输出报告 =====
  const videoSize = (fs.statSync(finalVideo).size / 1048576).toFixed(1);
  const videoDuration = getVideoDuration(finalVideo).toFixed(1);

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('\n🎉 全部完成！');
  console.log(`\n📹 输出视频: ${finalVideo}`);
  console.log(`   大小: ${videoSize} MB`);
  console.log(`   时长: ${videoDuration} 秒`);

  console.log('\n质量检查:');
  report.checks.forEach(c => {
    const icon = c.status === 'PASS' ? '✅' : c.status === 'FAIL' ? '❌' : c.status === 'WARN' ? '⚠️' : 'ℹ️';
    console.log(`   ${icon} ${c.item}: ${c.msg || ''}`);
  });

  // 生成 VIDEO_COMPLETE.md
  const completeMd = [
    `# 📹 视频生成完成报告`,
    ``,
    `## 基本信息`,
    `- 文件名: ${path.basename(finalVideo)}`,
    `- 大小: ${videoSize} MB`,
    `- 时长: ${videoDuration} 秒`,
    `- 分辨率: 1280×720`,
    `- 编码: H.264 + AAC`,
    `- PPT 页数: ${screenshots.length}`,
    ``,
    `## 质量检查结果`,
    ...report.checks.map(c => `- ${c.status === 'PASS' ? '✅' : c.status === 'FAIL' ? '❌' : '⚠️'} ${c.item}: ${c.msg || ''}`),
    ``,
    `## 生成时间`,
    `- ${new Date().toISOString()}`,
    ``,
  ].join('\n');

  fs.writeFileSync(path.join(outputDir, 'VIDEO_COMPLETE.md'), completeMd);
  console.log(`\n📄 完成报告: ${path.join(outputDir, 'VIDEO_COMPLETE.md')}`);

  // 清理
  if (args.cleanup) {
    console.log('\n=== 清理临时文件 ===');
    try {
      fs.rmSync(tempDir, { recursive: true, force: true });
      console.log('✅ 已清理临时目录');
    } catch (e) {
      console.warn(`⚠️  清理失败: ${e.message}`);
    }
  } else {
    console.log(`\n💡 临时目录保留: ${tempDir}`);
    console.log(`   使用 --cleanup 参数可自动清理`);
  }

  console.log();
}

// 启动
main().catch(err => {
  console.error('\n❌ 执行失败:', err.message);
  console.error(err.stack);
  process.exit(1);
});
