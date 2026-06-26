#!/usr/bin/env node
const QR_FILES = {
  auth: 'https://p0.pipi.cn/mediaplus/fe_rock_web/e429583d52977e4a18bd6d11feec25cee87c1.png?imageMogr2/thumbnail/2500x2500%3E',
  pay: 'https://p0.pipi.cn/mediaplus/fe_rock_web/e429583dfcf05184575b289615216d59ea89a.png?imageMogr2/thumbnail/2500x2500%3E'
};

async function main() {
  try {
    let inputData = '';
    process.stdin.setEncoding('utf8');
    for await (const chunk of process.stdin) inputData += chunk;

    const [inputText, fullParams] = JSON.parse(inputData);
    const context = fullParams?.context || {};
    const args = fullParams?.args || {};

    const channel = context.channel;
    const targetId = context.targetId;

    let qrType = args?.qrType;
    if (!qrType) {
      qrType = (inputText.includes("pay") || inputText.includes("支付")) ? "pay" : "auth";
    }

    const qrPath = QR_FILES[qrType];
    const isWeixin = channel && (channel.includes('weixin') || channel.includes('wx'));

    const linkUrl = qrType === "pay"
      ? (isWeixin
          ? 'https://deeplink.maoyan.com/asgard/app?type=weapp&to=%2Fpages%2Forder%2Findex%3FmerCode%3D1000545%26utm_source%3Dopenclaw'
          : 'https://m.maoyan.com/mtrade/order/list?merCode=1000545&utm_source=openclaw')
      : 'https://m.maoyan.com/mtrade/openclaw/token';

    const messageTitle = qrType === "pay" 
      ? "🎫 猫眼电影票支付" 
      : "🔐 猫眼登录认证";
    const linkText = qrType === "pay" ? "👉 点击前往支付" : "👉 点击获取认证密钥";
    const fullMessage = `${messageTitle}\n\n请长按识别二维码，或点击下方链接\n[${linkText}](${linkUrl})`;

    // 不再直接执行 shell，而是返回命令和参数供 AI 执行
    console.log(JSON.stringify({
      success: true,
      qrType,
      qrPath,
      fullMessage,
      // 如果 channel 和 targetId 存在，返回可直接执行的命令
      ...(channel && targetId ? {
        execCommand: `openclaw message send --channel ${channel} --target ${targetId} --media '${qrPath}' --message '${fullMessage.replace(/'/g, "'\\''")}'`
      } : {
        fallback: true,
        fallbackLink: linkUrl,
        message: "无渠道信息，请在文案末尾附加以下链接发送给用户"
      })
    }));

  } catch (e) {
    console.error(JSON.stringify({ error: e.message }));
  }
}

main();
