const axios = require('axios');
const crypto = require('crypto');

/**
 * 腾讯云 API v3 签名计算
 * @param {string} secretId - 腾讯云 SecretId
 * @param {string} secretKey - 腾讯云 SecretKey
 * @param {string} service - 服务名，固定为 "ocr"
 * @param {string} action - API 动作，固定为 "ArithmeticOCR"
 * @param {string} version - API 版本，固定为 "2018-11-19"
 * @param {string} region - 地域，可选 "ap-guangzhou"
 * @param {string} timestamp - 当前时间戳（秒）
 * @param {string} body - 请求体 JSON 字符串
 * @returns {string} Authorization 头
 */
function signV3(secretId, secretKey, service, action, version, region, timestamp, body) {
  const date = new Date(timestamp * 1000).toISOString().slice(0, 10).replace(/-/g, '');
  
  // 1. 拼接 CanonicalRequest
  const canonicalRequest = [
    'POST',
    '/',
    '',
    'content-type:application/json',
    'host:ocr.tencentcloudapi.com',
    '',
    'content-type;host',
    crypto.createHash('sha256').update(body).digest('hex')
  ].join('\n');

  // 2. 拼接待签名字符串
  const credentialScope = `${date}/${service}/tc3_request`;
  const hashedCanonicalRequest = crypto.createHash('sha256').update(canonicalRequest).digest('hex');
  const stringToSign = [
    'TC3-HMAC-SHA256',
    timestamp,
    credentialScope,
    hashedCanonicalRequest
  ].join('\n');

  // 3. 计算签名
  const secretDate = crypto.createHmac('sha256', 'TC3' + secretKey).update(date).digest();
  const secretService = crypto.createHmac('sha256', secretDate).update(service).digest();
  const secretSigning = crypto.createHmac('sha256', secretService).update('tc3_request').digest();
  const signature = crypto.createHmac('sha256', secretSigning).update(stringToSign).digest('hex');

  // 4. 拼接 Authorization
  return `TC3-HMAC-SHA256 Credential=${secretId}/${credentialScope}, SignedHeaders=content-type;host, Signature=${signature}`;
}

/**
 * 调用腾讯云 ArithmeticOCR API
 * @param {Object} params - 输入参数
 * @param {string} params.secretId - 腾讯云 SecretId
 * @param {string} params.secretKey - 腾讯云 SecretKey
 * @param {string} params.imageBase64 - 图片 Base64（可选）
 * @param {string} params.imageUrl - 图片 URL（可选）
 * @param {boolean} params.rejectNonArithmetic - 是否拒绝非算式图
 * @param {boolean} params.enableDispMidResult - 是否显示竖式中间结果
 * @returns {Promise<Object>} API 返回结果
 */
async function callArithmeticOCR(params) {
  const {
    secretId,
    secretKey,
    imageBase64,
    imageUrl,
    rejectNonArithmetic = false,
    enableDispMidResult = false
  } = params;

  if (!secretId || !secretKey) {
    throw new Error('请配置腾讯云 SecretId 和 SecretKey');
  }

  if (!imageBase64 && !imageUrl) {
    throw new Error('必须提供 imageBase64 或 imageUrl');
  }

  const timestamp = Math.floor(Date.now() / 1000);
  const service = 'ocr';
  const action = 'ArithmeticOCR';
  const version = '2018-11-19';
  const region = 'ap-guangzhou';

  // 构建请求体
  const payload = {
    ImageBase64: imageBase64,
    ImageUrl: imageUrl,
    RejectNonArithmeticPic: rejectNonArithmetic,
    EnableDispMidResult: enableDispMidResult
  };

  // 移除 undefined 字段
  Object.keys(payload).forEach(key => payload[key] === undefined && delete payload[key]);

  const body = JSON.stringify(payload);
  const authorization = signV3(secretId, secretKey, service, action, version, region, timestamp, body);

  try {
    const response = await axios({
      method: 'POST',
      url: 'https://ocr.tencentcloudapi.com',
      headers: {
        'Authorization': authorization,
        'Content-Type': 'application/json',
        'Host': 'ocr.tencentcloudapi.com',
        'X-TC-Action': action,
        'X-TC-Version': version,
        'X-TC-Timestamp': timestamp,
        'X-TC-Region': region,
        'X-TC-RequestClient': 'OpenClaw-Skill'
      },
      data: body,
      timeout: 10000
    });

    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`API 调用失败: ${JSON.stringify(error.response.data)}`);
    }
    throw error;
  }
}

/**
 * Skill 核心执行函数
 */
export default async function run(action, params) {
  try {
    if (action !== 'recognize-arithmetic') {
      return {
        success: false,
        message: `不支持的动作：${action}`,
        data: null
      };
    }

    // 从配置中读取腾讯云密钥（需要在 OpenClaw 配置中设置）
    const secretId = process.env.TENCENTCLOUD_SECRET_ID || params.secretId;
    const secretKey = process.env.TENCENTCLOUD_SECRET_KEY || params.secretKey;

    const {
      imageBase64,
      imageUrl,
      rejectNonArithmetic,
      enableDispMidResult
    } = params;

    // 调用 API
    const result = await callArithmeticOCR({
      secretId,
      secretKey,
      imageBase64,
      imageUrl,
      rejectNonArithmetic,
      enableDispMidResult
    });

    // 检查 API 返回是否有错误
    if (result.Response?.Error) {
      return {
        success: false,
        message: `腾讯云 API 错误: ${result.Response.Error.Message} (Code: ${result.Response.Error.Code})`,
        data: result.Response
      };
    }

    // 提取识别结果
    const textDetections = result.Response?.TextDetections || [];
    
    // 格式化输出，便于 AI 理解
    const formattedResults = textDetections.map(item => ({
      text: item.DetectedText,
      confidence: item.Confidence,
      polygon: item.Polygon,
      advancedInfo: item.AdvancedInfo ? JSON.parse(item.AdvancedInfo) : null
    }));

    // 提取所有识别出的文本（用于快速查看）
    const allText = textDetections.map(t => t.DetectedText).join(' ');

    return {
      success: true,
      message: `成功识别算式，共检测到 ${textDetections.length} 个文本区域`,
      data: {
        raw: result.Response,
        textDetections: formattedResults,
        allText: allText,
        angle: result.Response?.Angle || 0,
        requestId: result.Response?.RequestId
      }
    };

  } catch (error) {
    return {
      success: false,
      message: `执行失败：${error.message}`,
      data: null
    };
  }
}
