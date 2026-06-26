#!/usr/bin/env node

const { LiblibAIClient } = require('../lib/client');
const fs = require('fs');
const path = require('path');

// 简单的参数解析
function parseOptions(arr) {
  const options = {};
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].startsWith('-')) {
      let key = arr[i].replace(/^-+/, '');
      if (key.includes('=')) {
        const [k, v] = key.split('=');
        options[k] = v;
      } else {
        // 检查是否是需要值的选项
        if (['p', 'prompt', 'n', 'negative-prompt', 'W', 'width', 'H', 'height',
             's', 'steps', 'c', 'cfg-scale', 'sampler', 'seed', 'i', 'img-count',
             't', 'template-uuid', 'S', 'source-image', 'd', 'denoising-strength',
             'resize-mode', 'mask-image', 'mask-mode', 'inpaint-area',
             'additional-network', 'controlnet', 'hires-steps', 'hires-denoising',
             'hires-upscaler', 'hires-width', 'hires-height', 'controlnet-type',
             'controlnet-image', 'aspect-ratio', 'a', 'randn-source', 'restore-faces'].includes(key)
            || key.startsWith('hires-') || key.startsWith('controlnet-')) {
          // 下一个参数是值
          options[key] = arr[i + 1];
          i++;
        } else {
          // 布尔标记
          options[key] = true;
        }
      }
    }
  }
  return options;
}

// 格式化输出，便于复制
function formatResult(result) {
  // 提取关键信息
  const output = [];

  if (result.generateUuid) {
    output.push(`UUID: ${result.generateUuid}`);
  }

  if (result.images && result.images.length > 0) {
    output.push('生成的图片:');
    result.images.forEach((img, idx) => {
      output.push(`[${idx + 1}] ${img.imageUrl}`);
    });
  }

  if (result.videos && result.videos.length > 0) {
    output.push('生成的视频:');
    result.videos.forEach((vid, idx) => {
      output.push(`[${idx + 1}] ${vid.videoUrl}`);
    });
  }

  // 状态信息
  output.push(`状态: ${result.generateStatus} (${getStatusText(result.generateStatus)})`);
  if (result.percentCompleted) {
    output.push(`进度: ${result.percentCompleted}%`);
  }

  // 费用信息
  if (result.pointsCost !== undefined) {
    output.push(`消耗积分: ${result.pointsCost}`);
  }
  if (result.accountBalance !== undefined) {
    output.push(`剩余积分: ${result.accountBalance}`);
  }

  return output.join('\n');
}

function getStatusText(status) {
  const statusMap = {
    1: '待处理',
    2: '处理中',
    3: '已生成',
    4: '审核中',
    5: '成功',
    6: '失败',
    7: '超时'
  };
  return statusMap[status] || '未知';
}

// 简化的 CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    console.log(`
liblibai - LiblibAI 图像生成命令行工具

用法:
  liblibai <command> [options]

命令:
  text2img           从文本生成图像
  text2img-ultra     使用 Ultra 模型生成图像
  img2img            基于现有图像生成新图像
  upload <file>      上传本地文件到 LiblibAI
  status <uuid>      检查任务状态
  wait <uuid>        等待任务完成并获取结果

示例:
  liblibai text2img -p "一只可爱的小狗" -W 1024 -H 1024
  liblibai upload image.jpg
  liblibai wait <uuid>
    `);
    return;
  }

  const options = parseOptions(args.slice(1));

  try {
    const client = new LiblibAIClient();

    switch (command) {
      case 'text2img':
        if (!options.p) {
          console.error('错误: 必须提供 -p/--prompt 参数');
          process.exit(1);
        }

        const params = {
          templateUuid: options.t,
          generateParams: {
            width: parseInt(options.W) || 768,
            height: parseInt(options.H) || 1024,
            steps: parseInt(options.s) || 20,
            cfgScale: parseFloat(options.c) || 7,
            sampler: parseInt(options.sampler) || 15,
            seed: parseInt(options.seed) || -1,
            imgCount: parseInt(options.i) || 1,
            randnSource: parseInt(options['randn-source']) || 0,
            restoreFaces: parseInt(options['restore-faces']) || 0,
            prompt: options.p,
            negativePrompt: options.n,
          }
        };

        if (options['additional-network']) {
          params.generateParams.additionalNetwork = JSON.parse(options['additional-network']);
        }

        if (options.hires) {
          params.generateParams.hiResFixInfo = {
            hiresSteps: parseInt(options['hires-steps']) || 20,
            hiresDenoisingStrength: parseFloat(options['hires-denoising']) || 0.75,
            upscaler: parseInt(options['hires-upscaler']) || 10,
          };
          if (options['hires-width'] && options['hires-height']) {
            params.generateParams.hiResFixInfo.resizedWidth = parseInt(options['hires-width']);
            params.generateParams.hiResFixInfo.resizedHeight = parseInt(options['hires-height']);
          }
        }

        if (options.controlnet) {
          params.generateParams.controlNet = JSON.parse(options.controlnet);
        }

        console.log('正在生成图像...');
        const result = await client.text2img(params);
        console.log('\n' + formatResult(result) + '\n');
        break;

      case 'upload':
        const file = args[1];
        if (!file) {
          console.error('错误: 必须提供文件路径');
          process.exit(1);
        }
        if (!fs.existsSync(file)) {
          console.error('错误: 文件不存在:', file);
          process.exit(1);
        }
        const fileBuffer = fs.readFileSync(file);
        const filename = options.name || path.basename(file);
        console.log(`正在上传 ${filename}...`);
        const uploadResult = await client.uploadFile(fileBuffer, filename);
        console.log('上传成功:', uploadResult);
        break;

      case 'status':
        const uuid = args[1];
        if (!uuid) {
          console.error('错误: 必须提供 UUID');
          process.exit(1);
        }
        const statusResult = await client.getStatus(uuid);
        console.log('\n' + formatResult(statusResult) + '\n');
        break;

      case 'wait':
        const waitUuid = args[1];
        if (!waitUuid) {
          console.error('错误: 必须提供 UUID');
          process.exit(1);
        }
        const interval = parseInt(options.interval) || 3000;
        const timeout = parseInt(options.timeout) || 300000;
        console.log('等待任务完成...');
        const waitResult = await client.waitResult(waitUuid, interval, timeout);
        console.log('\n' + formatResult(waitResult) + '\n');
        break;

      default:
        console.error(`未知命令: ${command}`);
        process.exit(1);
    }
  } catch (error) {
    console.error('错误:', error.message);
    process.exit(1);
  }
}

main();
