#!/usr/bin/env node
// md2pdf-puppet.js — markdown → PDF (Typora 同款方案:Puppeteer 调 headless Chrome 打印)
//
// 用法:
//   node md2pdf-puppet.js <input.md> [output.pdf] [options]
//
// 选项:
//   --theme <name>       主题(typora-newsprint / typora-night / github / academic / huo15-brand)
//   --paper <size>       A4 / Letter / A3 / A5(默认 A4)
//   --margin <mm>        四边等距(默认 18)
//   --no-mermaid         跳过 mermaid 渲染等待(纯文档时更快)
//   --print-urls         链接后追加 URL 文本
//   --header <text>      自定义页眉(覆盖主题默认)
//   --footer <text>      自定义页脚(支持 {pageNumber} {totalPages})
//   --qr-url <url>       PDF 页脚右下角嵌入二维码(扫码 → url),典型用法:把
//                        enhance_share_file 拿到的 share URL 嵌入打印版,实现"线下纸质 → 线上文档"
//   --qr-label <text>    二维码旁的文字说明(默认"扫码看在线版")
//   --og-title TEXT      OG meta(让 PDF 生成同时也能输出带卡片预览的 HTML 中间产物;PDF 本身不显示)

const fs = require('fs');
const path = require('path');
const { buildHtml, buildQrSvgDataUrl, AVAILABLE_THEMES } = require('./lib/render.js');

function parseArgs(argv) {
  const args = { positional: [], opts: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args.opts[key] = true;
      } else {
        args.opts[key] = next;
        i++;
      }
    } else {
      args.positional.push(a);
    }
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const [inputPath, outputPath] = args.positional;

  if (!inputPath) {
    console.error('用法: md2pdf-puppet.js <input.md> [output.pdf] [--theme typora-newsprint] [--paper A4] [--margin 18]');
    console.error('主题: ' + AVAILABLE_THEMES.join(' / '));
    process.exit(1);
  }
  if (!fs.existsSync(inputPath)) {
    console.error(`找不到输入文件: ${inputPath}`);
    process.exit(1);
  }

  const theme = args.opts.theme || 'apple-tech';
  const paper = args.opts.paper || 'A4';
  const margin = parseInt(args.opts.margin || '18', 10);
  const out = outputPath || inputPath.replace(/\.md$/, '.pdf');
  const printUrls = !!args.opts['print-urls'];
  const includeMermaid = !args.opts['no-mermaid'];

  const markdown = fs.readFileSync(inputPath, 'utf8');
  const title = path.basename(inputPath, '.md');

  const html = buildHtml({
    markdown,
    theme,
    title,
    includePrint: true,
    includeMermaid,
  });

  const finalHtml = printUrls
    ? html.replace('<body class=', '<body data-print-urls="1" class="print-show-urls ').replace('class="print-show-urls class=', 'class="print-show-urls ')
    : html;

  let puppeteer;
  try {
    puppeteer = require('puppeteer');
  } catch (_) {
    console.error('未安装 puppeteer。请先在 skill 目录运行: npm install');
    process.exit(2);
  }

  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setContent(finalHtml, { waitUntil: 'networkidle0', timeout: 60000 });

    if (includeMermaid && finalHtml.includes('class="mermaid"')) {
      // 等 mermaid 渲染完(最多 5 秒)
      await page.waitForFunction(() => {
        const els = document.querySelectorAll('.mermaid');
        if (!els.length) return true;
        return Array.from(els).every(el => el.querySelector('svg'));
      }, { timeout: 5000 }).catch(() => { /* 渲染失败也继续,不卡死 */ });
    }

    const pdfOpts = {
      path: out,
      format: paper,
      printBackground: true,
      margin: {
        top: `${margin}mm`,
        right: `${margin}mm`,
        bottom: `${margin}mm`,
        left: `${margin}mm`,
      },
    };

    const qrUrl = args.opts['qr-url'];
    const qrLabel = args.opts['qr-label'] || '扫码看在线版';
    let qrDataUrl = null;
    if (qrUrl) {
      try {
        qrDataUrl = await buildQrSvgDataUrl(qrUrl, { width: 60, margin: 0 });
      } catch (e) {
        console.error(`× 二维码生成失败(可能未安装 qrcode 包):${e.message}`);
        qrDataUrl = null;
      }
    }

    if (args.opts.header || args.opts.footer || qrDataUrl) {
      pdfOpts.displayHeaderFooter = true;
      pdfOpts.headerTemplate = args.opts.header
        ? `<div style="font-size:9pt;color:#999;width:100%;text-align:center;font-family:'PingFang SC',sans-serif">${escapeHtml(args.opts.header)}</div>`
        : '<div></div>';

      let footerHtml;
      if (qrDataUrl) {
        // 二维码模式:左侧文字(可含 footer 自定义)+ 右侧二维码 + 标注
        const leftText = args.opts.footer
          ? args.opts.footer.replace('{pageNumber}', '<span class="pageNumber"></span>').replace('{totalPages}', '<span class="totalPages"></span>')
          : '青岛火一五信息科技 · <span class="pageNumber"></span> / <span class="totalPages"></span>';
        footerHtml = `<div style="font-size:9pt;color:#666;width:100%;display:flex;align-items:center;justify-content:space-between;padding:0 18mm;font-family:'PingFang SC','Helvetica Neue',sans-serif">
  <div style="flex:1">${leftText}</div>
  <div style="display:flex;align-items:center;gap:6px">
    <span style="color:#999;font-size:8pt">${escapeHtml(qrLabel)}</span>
    <img src="${qrDataUrl}" style="height:42px;width:42px;display:block">
  </div>
</div>`;
      } else {
        footerHtml = args.opts.footer
          ? `<div style="font-size:9pt;color:#999;width:100%;text-align:center;font-family:'PingFang SC',sans-serif">${args.opts.footer.replace('{pageNumber}', '<span class="pageNumber"></span>').replace('{totalPages}', '<span class="totalPages"></span>')}</div>`
          : '<div></div>';
      }
      pdfOpts.footerTemplate = footerHtml;

      pdfOpts.margin.top = `${margin + 8}mm`;
      pdfOpts.margin.bottom = qrDataUrl ? `${margin + 18}mm` : `${margin + 8}mm`;
    }

    await page.pdf(pdfOpts);
    const qrTag = qrDataUrl ? `  +qr` : '';
    console.error(`✓ ${out}  (theme=${theme}  paper=${paper}  margin=${margin}mm${qrTag})`);
  } finally {
    await browser.close();
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

main().catch(err => { console.error(err); process.exit(2); });
