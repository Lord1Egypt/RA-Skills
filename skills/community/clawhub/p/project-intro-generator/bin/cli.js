#!/usr/bin/env node
const path = require('path');
const { generateIntro, generateLongImage, THEMES } = require('../src');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith('--no-')) {
      const key = arg.replace(/^--no-/, '');
      args[key] = false;
      continue;
    }
    if (arg.startsWith('--')) {
      const key = arg.replace(/^--/, '');
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        if (next === 'false' || next === '0') {
          args[key] = false;
        } else {
          args[key] = next;
        }
        i += 1;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

function printHelp() {
  const themeKeys = Object.keys(THEMES).join(', ');
  console.log(`project-intro-generator - 一键生成项目介绍页

使用：
  project-intro-generator --project <路径> [--out <输出HTML>] [--theme ${themeKeys}] [--accent #RRGGBB] [--export-image|--no-export-image --image-out <png>]
  project-intro-generator --html <已存在的HTML路径> [--image-out <png>]

示例：
  project-intro-generator --project . --theme aurora
  project-intro-generator --html ./介绍.html --image-out ./介绍.png
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h) {
    printHelp();
    return;
  }

  const cwd = process.cwd();
  const htmlInput = args.html;
  if (htmlInput) {
    const resolvedHtml = path.resolve(htmlInput);
    const imageOut = args['image-out'] ? path.resolve(args['image-out']) : path.join(path.dirname(resolvedHtml), `${path.basename(resolvedHtml, path.extname(resolvedHtml))}.png`);
    try {
      const image = await generateLongImage(resolvedHtml, imageOut, {});
      console.log(`已根据 HTML 导出长图：${image.imagePath}`);
    } catch (imageErr) {
      console.error(`导出长图失败：${imageErr.message}`);
      process.exitCode = 1;
    }
    return;
  }

  const projectPath = args.project ? path.resolve(args.project) : cwd;
  const gitUrl = args.git;
  const outputPath = args.out ? path.resolve(args.out) : (gitUrl ? path.join(cwd, '介绍.html') : path.join(projectPath, '介绍.html'));
  const theme = args.theme || 'aurora';
  const accent = args.accent;
  const exportImage = args['export-image'] === false ? false : args.exportImage === false ? false : true;
  const imageOut = args['image-out'] ? path.resolve(args['image-out']) : (gitUrl ? path.join(cwd, '介绍.png') : path.join(projectPath, '介绍.png'));

  try {
    const result = await generateIntro({ projectPath, gitUrl, outputPath, theme, accent, imageOut });
    console.log(`已生成 HTML：${result.htmlPath}（主题：${result.theme}）`);

    if (exportImage) {
      try {
        const image = await generateLongImage(result.htmlPath, imageOut, {});
        console.log(`已导出长图：${image.imagePath}`);
      } catch (imageErr) {
        console.error(`导出长图失败：${imageErr.message}`);
        process.exitCode = 1;
      }
    }
  } catch (err) {
    console.error(`生成失败：${err.message}`);
    process.exitCode = 1;
  }
}

main();
