import fs from 'fs';
import path from 'path';
import {
  downloadOssFile,
  formatProgress,
  formatSize,
  extractFileId,
  resolveOssPath,
  getLocalFilePath,
  isFileDownloaded,
  colors,
  log,
  info
} from '../utils.js';

const error = console.error;

export async function downloadFiles(fileUrls, options = {}) {
  const {
    entityType = 'unknown',
    apiKey,
    useThumbnail = true,
    verbose = false
  } = options;

  const concurrency = 3;

  const results = {
    successful: [],
    skipped: [],
    nonexistent: []
  };

  const nonexistentFiles = [];

  if (verbose) {
    info(`\n会记录不存在的文件，以便后续处理:\n`);
  }

  let successfulCount = 0;
  let skippedCount = 0;
  let nonexistentCount = 0;

  const processQueue = (queue) => {
    return queue.reduce(async (promiseChain, fileUrl) => {
      return promiseChain.then(async () => {
        try {
          const ossUrl = resolveOssPath(fileUrl, useThumbnail);
          const fileId = extractFileId(ossUrl);
          const localPath = getLocalFilePath(entityType, fileId, useThumbnail);

          const thumbFilename = `${fileId.replace(/\.(jpg|png|jpeg|gif|webp)$/i, '')}_${useThumbnail ? 'thumb' : 'original'}.${fileId.includes('.') ? fileId.split('.').pop() : 'jpg'}`;

          if (isFileDownloaded(entityType, fileId, useThumbnail)) {
            if (verbose) {
              info(`   ${colors.yellow}⏭️  ${colors.reset} 跳过: ${thumbFilename}`);
            }
            results.skipped.push({
              url: fileUrl,
              localPath: localPath,
              fileId: fileId
            });
            skippedCount++;
          } else {
            if (verbose) {
              info(`\n   ${colors.blue}📥 ${colors.reset} ${thumbFilename}`);
            }

            const startTime = Date.now();
            let downloaded = 0;
            let total = 0;
            let percent = 0;

            try {
              await new Promise((resolve, reject) => {
                downloadOssFile(ossUrl, localPath, (currentDownloaded, currentTotal) => {
                  downloaded = currentDownloaded;
                  total = currentTotal;
                  percent = Math.round((downloaded / total) * 100);
                  process.stdout.write(`\r${formatProgress(downloaded, total, percent)}`);
                }).then(() => {
                  resolve();
                }).catch(reject);
              });

              const duration = ((Date.now() - startTime) / 1000).toFixed(2);

              if (verbose) {
                console.log(` ${colors.green}✓${colors.reset} (${formatSize(fs.statSync(localPath).size)}, ${duration}秒)`);
              }

              results.successful.push({
                url: fileUrl,
                localPath: localPath,
                duration: duration,
                ossUrl: ossUrl,
                fileId: fileId,
                fileCount: 1
              });

              successfulCount++;

            } catch (downloadError) {
              if (verbose) {
                console.log(` ${colors.red}✗${colors.reset} (${downloadError.message})`);
              }

              results.nonexistent.push({
                url: fileUrl,
                ossUrl: ossUrl,
                fileId: fileId,
                error: `[HTTP ${downloadError.statusCode || 404}]: ${downloadError.message}`
              });

              nonexistentCount++;

              if (!nonexistentFiles.find(f => f.ossUrl === ossUrl)) {
                nonexistentFiles.push({
                  ossUrl: ossUrl,
                  fileId: fileId,
                  thumbFilename: thumbFilename
                });
              }
            }
          }

          printProgressBar(successfulCount, skippedCount, nonexistentCount);

        } catch (error) {
          results.nonexistent.push({
            url: fileUrl,
            error: `[错误]: ${error.message}`,
            ossUrl: '',
            fileId: ''
          });

          nonexistentCount++;
          printProgressBar(successfulCount, skippedCount, nonexistentCount);
        }
      });
    }, Promise.resolve());
  };

  try {
    await processQueue(fileUrls);
  } catch (error) {
    error(`\n⚠️  下载过程中发生错误: ${error.message}`);
  }

  console.log('\n');

  log(colors.bright, `\n📊 批量下载完成!\n`);

  log(colors.green, `✅ 成功: ${colors.bright}${successfulCount}/${fileUrls.length}`);
  if (skippedCount > 0) {
    log(colors.yellow, `⏭️  跳过: ${colors.bright}${skippedCount}/${fileUrls.length}`);
  }
  if (nonexistentCount > 0) {
    log(colors.red, `⚠️  不存在: ${colors.bright}${nonexistentCount}/${fileUrls.length}`);
  }

  log(colors.dim, '');

  if (successfulCount > 0) {
    const totalTime = results.successful.reduce((sum, r) => sum + parseFloat(r.duration), 0);
    log(colors.bright, `   总耗时: ${totalTime.toFixed(2)}秒`);
    log(colors.bright, `   平均速度: ${(fileUrls.length / totalTime).toFixed(2)} 文件/秒`);
    log(colors.bright, `   实际下载: ${formatSize(results.successful.reduce((sum, r) => sum + fs.statSync(r.localPath).size, 0))}`);
  }

  log(colors.dim, '');

  if (nonexistentCount > 0) {
    log(colors.red, `\n⚠️  不存在的文件 (${nonexistentCount}个):\n`);
    results.nonexistent.forEach((result, index) => {
      log(colors.red, `   ${index + 1}. ${result.url}`);
      if (result.ossUrl) {
        log(colors.red.dim, `      OSS路径: ${result.ossUrl}`);
      }
      if (result.fileId) {
        log(colors.red.dim, `      文件ID: ${result.fileId}`);
      }
      log(colors.red.dim, `      错误: ${result.error}\n`);
    });

    log(colors.bright.dim, `\n💡 已记录不存在的文件 (共${nonexistentFiles.length}个):\n`);
    nonexistentFiles.forEach((file, index) => {
      log(colors.bright.dim, `   ${index + 1}. ${file.ossUrl}`);
      log(colors.bright.dim, `      文件: ${file.thumbFilename}\n`);
    });
  }

  return results;
}

function printProgressBar(successful, skipped, nonexistent) {
  const total = successful + skipped + nonexistent;
  const barWidth = 40;
  const filledWidth = Math.floor((successful / total) * barWidth);
  const bar = '█'.repeat(filledWidth) + '░'.repeat(barWidth - filledWidth);

  process.stdout.write(`\r[${bar}] ${successful}✅ ${skipped}⏭️  ${nonexistent}⚠️`);
}

export async function downloadFile(fileUrl, options) {
  return new Promise((resolve, reject) => {
    const {
      entityType = 'unknown',
      apiKey,
      useThumbnail = true,
      verbose = false
    } = options;

    results.nonexistent = [];

    const ossUrl = resolveOssPath(fileUrl, useThumbnail);
    const fileId = extractFileId(ossUrl);
    const localPath = getLocalFilePath(entityType, fileId, useThumbnail);

    const thumbFilename = `${fileId.replace(/\.(jpg|png|jpeg|gif|webp)$/i, '')}_${useThumbnail ? 'thumb' : 'original'}.${fileId.includes('.') ? fileId.split('.').pop() : 'jpg'}`;

    if (isFileDownloaded(entityType, fileId, useThumbnail)) {
      resolve(localPath);
      return;
    }

    const startTime = Date.now();
    let downloaded = 0;
    let total = 0;
    let percent = 0;

    downloadOssFile(ossUrl, localPath, (currentDownloaded, currentTotal) => {
      downloaded = currentDownloaded;
      total = currentTotal;
      percent = Math.round((downloaded / total) * 100);
      process.stdout.write(`\r${formatProgress(downloaded, total, percent)}`);
    }).then(() => {
      if (verbose) {
        console.log(` ${colors.green}✓${colors.reset} (${formatSize(fs.statSync(localPath).size)}, ${((Date.now() - startTime) / 1000).toFixed(2)}秒)`);
      }
      resolve(localPath);
    }).catch((error) => {
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      reject({
        message: `[HTTP ${error.statusCode || error.code}]: ${error.message}`,
        ossUrl: ossUrl,
        fileId: fileId
      });
    });
  });
}