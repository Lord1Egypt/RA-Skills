/**
 * 配置验证工具
 */

function hasValue(value) {
  return value !== undefined && value !== null && value !== '';
}

// 验证 App ID 格式
function validateAppId(appId) {
  return /^cli_[a-zA-Z0-9]+$/.test(appId);
}

// 验证账户 ID 格式
function validateAccountId(id) {
  return /^[a-z0-9-]+$/.test(id);
}

// 验证群聊 ID 格式
function validateChatId(id) {
  return /^oc_[a-zA-Z0-9]+$/.test(id);
}

// 验证用户 ID 格式
function validateUserId(id) {
  return /^ou_[a-zA-Z0-9]+$/.test(id);
}

function validateBinding(binding, index) {
  const errors = [];
  const label = `binding[${index}]`;

  if (!binding?.agentId) {
    errors.push(`${label} 缺少 agentId`);
  }

  const match = binding?.match;
  if (!match?.channel) {
    errors.push(`${label} 缺少 match.channel`);
    return errors;
  }

  if (hasValue(match.accountId)) {
    if (!validateAccountId(match.accountId)) {
      errors.push(`${label} accountId 格式无效: ${match.accountId}`);
    }
    return errors;
  }

  if (match?.peer?.kind === 'group' && hasValue(match?.peer?.id)) {
    if (!validateChatId(match.peer.id)) {
      errors.push(`${label} 群聊 ID 格式无效: ${match.peer.id}`);
    }
    return errors;
  }

  errors.push(`${label} 必须配置 accountId 或 group peer.id`);
  return errors;
}

// 验证完整配置
function validateConfig(config) {
  const errors = [];
  
  if (!config.channels?.feishu) {
    errors.push('缺少 channels.feishu 配置');
    return errors;
  }
  
  const accounts = config.channels.feishu.accounts || {};
  
  for (const [key, acc] of Object.entries(accounts)) {
    if (!validateAccountId(key)) {
      errors.push(`账户 ID "${key}" 格式无效`);
    }
    if (!validateAppId(acc.appId)) {
      errors.push(`[${key}] App ID 格式无效: ${acc.appId}`);
    }
    if (!acc.appSecret) {
      errors.push(`[${key}] App Secret 不能为空`);
    }
  }
  
  const bindings = config.bindings || [];
  bindings.forEach((binding, index) => {
    errors.push(...validateBinding(binding, index));
  });
  
  return errors;
}

module.exports = {
  validateAppId,
  validateAccountId,
  validateChatId,
  validateUserId,
  validateConfig,
  validateBinding
};
