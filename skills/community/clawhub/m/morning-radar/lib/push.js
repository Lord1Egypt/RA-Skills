/**
 * 飞书推送模块
 */

export async function getTenantToken(appId, appSecret) {
  const response = await fetch("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret })
  });
  
  const data = await response.json();
  if (data.code !== 0) {
    throw new Error(`获取token失败: ${data.msg}`);
  }
  return data.tenant_access_token;
}

export async function sendMessage(token, openId, message) {
  const response = await fetch("https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      receive_id: openId,
      msg_type: "text",
      content: JSON.stringify({ text: message })
    })
  });
  
  const data = await response.json();
  if (data.code !== 0) {
    throw new Error(`发送消息失败: ${data.msg}`);
  }
  return data;
}

export async function pushToFeishu(config, message) {
  const token = await getTenantToken(config.appId, config.appSecret);
  await sendMessage(token, config.receiverOpenId, message);
}
