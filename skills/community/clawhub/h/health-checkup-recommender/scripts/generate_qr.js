/**
 * generate_qr.js - 本地二维码生成脚本
 * 
 * ═══════════════════════════════════════════════════════════════
 * 网络请求透明度声明
 * ═══════════════════════════════════════════════════════════════
 * 
 * 【无网络请求】
 * 本脚本不发起任何网络请求。
 * 
 * 【二维码内容】
 * 二维码包含以下 URL 参数：
 *   - welfareid: 服务器返回的脱敏福利ID（由 sync_items.js 获取）
 *   - ruleid: 服务器返回的脱敏规则ID（由 sync_items.js 获取）
 *   - urlsrc: 固定值 'brief'，用于区分入口类型
 * 
 * 【不包含任何PII】
 * 二维码仅包含脱敏的业务ID，不包含姓名、手机号、身份证等信息。
 * 用户的真实个人信息在扫码后由用户自行在第三方平台授权。
 * 
 * 【同意要求】
 *   - 必须提供 --consent=true 参数，否则拒绝执行
 * 
 * ═══════════════════════════════════════════════════════════════
 * 
 * 使用方式：
 *   node scripts/generate_qr.js --consent=true <output_path> <welfareid> <ruleid>
 *   示例：node scripts/generate_qr.js --consent=true output.png w123 r456
 */

const QRCode = require('qrcode')
const fs = require('fs')
const path = require('path')
const apiConfig = require('../config/api')

/**
 * 生成预约提示文本（将放入二维码的内容）
 * 
 * @param {Object} pkg - 参数信息
 * @param {string} pkg.welfareid - 服务器返回的脱敏福利ID
 * @param {string} pkg.ruleid - 服务器返回的脱敏规则ID
 * @returns {string} 带参数的预约链接
 * 
 * 【隐私保证】
 * welfareid 和 ruleid 是服务器生成的脱敏ID，不包含任何用户个人信息
 */
function buildQRContent(pkg) {
  const { welfareid, ruleid } = pkg
  
  // ───────────────────────────────────────────────────────────
  // URL 格式：https://www.ihaola.com.cn/launch/haola/pe?urlsrc=brief&welfareid=xxx&ruleid=yyy
  // 仅包含脱敏业务ID，无任何PII
  // ───────────────────────────────────────────────────────────
  const url = new URL('/launch/haola/pe', apiConfig.domain)
  url.searchParams.append('urlsrc', 'brief')
  if (welfareid) {
    url.searchParams.append('welfareid', welfareid)
  }
  if (ruleid) {
    url.searchParams.append('ruleid', ruleid)
  }
  
  return url.toString()
}

/**
 * 生成二维码图片（本地保存）
 * 
 * @param {string} outputPath - 输出路径
 * @param {Object} pkg - 参数信息
 * 
 * 【输出】
 *   - 生成 PNG 格式二维码图片文件（本地保存）
 *   - 不上传任何数据到服务器
 */
async function generateQR(outputPath, pkg) {
  if (!outputPath) {
    outputPath = path.join(__dirname, '..', '体检预约二维码.png')
  }
  outputPath = path.resolve(outputPath)

  const qrContent = buildQRContent(pkg)

  const opts = {
    errorCorrectionLevel: 'M',
    type: 'image/png',
    margin: 3,
    width: 400,
    color: {
      dark: '#1a3a5c',
      light: '#ffffff'
    }
  }

  // 【关键】仅生成图片，不发送网络请求
  await QRCode.toFile(outputPath, qrContent, opts)
  const stats = fs.statSync(outputPath)
  console.log(`QR saved: ${outputPath} (${Math.round(stats.size / 1024)} KB)`)
  console.log(`Content preview:\n${qrContent}`)
  return { path: outputPath, content: qrContent }
}

// ═══════════════════════════════════════════════════════════════
// CLI 执行入口
// ═══════════════════════════════════════════════════════════════
if (require.main === module) {
  const args = process.argv.slice(2)
  
  // --consent 参数检查（必须）
  const consentIndex = args.findIndex(arg => arg === '--consent=true' || arg === '--consent')
  const hasConsent = consentIndex !== -1
  if (!hasConsent) {
    console.error('❌ 拒绝执行: 必须提供 --consent=true 参数')
    process.exit(1)
  }

  if (consentIndex !== -1) {
    args.splice(consentIndex, 1)
  }

  if (args.length === 0) {
    console.log('用法: node generate_qr.js --consent=true [output_path] [welfareid] [ruleid]')

    generateQR(path.join(__dirname, '..', '体检预约_demo.png'), {
      welfareid: 'demo_w',
      ruleid: 'demo_r'
    }).catch(e => { 
      console.error(e)
      process.exit(1)
    })
    return
  }

  const outputPath = args[0]
  const welfareid = args[1]
  const ruleid = args[2]

  generateQR(outputPath, { 
    welfareid,
    ruleid
  }).catch(e => {
    console.error(e)
    process.exit(1)
  })
}

async function generateQRDataUri(pkg) {
  const qrContent = buildQRContent(pkg);
  return QRCode.toDataURL(qrContent, {
    errorCorrectionLevel: 'M',
    margin: 3,
    width: 400,
    color: { dark: '#1a3a5c', light: '#ffffff' }
  });
}

module.exports = { buildQRContent, generateQR, generateQRDataUri }
