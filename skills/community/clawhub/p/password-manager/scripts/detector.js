/**
 * detector.js - Sensitive Information Detection Module
 * 
 * Detects sensitive information in text (tokens, passwords, API keys, etc.)
 */

// Detection rules
const DETECTION_RULES = {
  github_token: {
    pattern: /ghp_[a-zA-Z0-9]{36}/g,
    name: 'GitHub Token',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'github-token'
  },
  gitlab_token: {
    pattern: /glpat-[a-zA-Z0-9_-]{20,}/g,
    name: 'GitLab Token',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'gitlab-token'
  },
  aws_key: {
    pattern: /AKIA[0-9A-Z]{16}/g,
    name: 'AWS Access Key',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'aws-key'
  },
  aws_secret: {
    // Fix: Add context limit to avoid matching arbitrary 40-char strings
    pattern: /(?:aws_secret|secret_access_key|AWS_SECRET)[=:\s]*["']?([A-Za-z0-9/+=]{40})["']?/gi,
    name: 'AWS Secret Key',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'aws-secret'
  },
  openai_key: {
    pattern: /sk-[a-zA-Z0-9]{48}/g,
    name: 'OpenAI API Key',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'openai-key'
  },
  aliyun_key: {
    pattern: /LTAI[a-zA-Z0-9]{12,}/g,
    name: 'Aliyun AccessKey',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'aliyun-key'
  },
  password_context: {
    pattern: /密码 [是：:]\s*["']?([^\s"'",;]{8,})["']?/gi,
    name: 'Password (Chinese)',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'password'
  },
  password_context_en: {
    pattern: /password[is:]\s*["']?([^\s"'",;]{8,})["']?/gi,
    name: 'Password',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'password'
  },
  generic_api_key: {
    pattern: /api[_-]?key[=:\s]*["']?([a-zA-Z0-9_-]{20,})["']?/gi,
    name: 'API Key',
    sensitivity: 'medium',
    autoAsk: true,
    suggestedEntryName: 'api-key'
  },
  jwt_token: {
    pattern: /eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*/g,
    name: 'JWT Token',
    sensitivity: 'medium',
    autoAsk: true,
    suggestedEntryName: 'jwt-token'
  },
  bearer_token: {
    pattern: /bearer\s+[a-zA-Z0-9_-]{20,}/gi,
    name: 'Bearer Token',
    sensitivity: 'medium',
    autoAsk: true,
    suggestedEntryName: 'bearer-token'
  },
  private_key: {
    pattern: /-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----/g,
    name: 'Private Key',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'private-key'
  },
  connection_string: {
    pattern: /(?:mongodb|postgres|mysql|redis):\/\/[^\s'"]+/gi,
    name: 'Database Connection String',
    sensitivity: 'high',
    autoAsk: true,
    suggestedEntryName: 'db-connection'
  }
};

/**
 * Detect sensitive information in text
 * @param {string} text - Text to detect
 * @param {Object} config - Configuration options
 * @returns {Array} - Detection results array
 */
export function detect(text, config = {}) {
  const {
    sensitivityThreshold = 'medium',
    enabled = true
  } = config;
  
  if (!enabled) {
    return [];
  }
  
  const results = [];
  const sensitivityLevels = { high: 3, medium: 2, low: 1 };
  const threshold = sensitivityLevels[sensitivityThreshold] || 2;
  
  for (const [type, rule] of Object.entries(DETECTION_RULES)) {
    // Reset regex
    rule.pattern.lastIndex = 0;
    
    let match;
    while ((match = rule.pattern.exec(text)) !== null) {
      // Check if threshold is met
      const meetsThreshold = sensitivityLevels[rule.sensitivity] >= threshold;
      
      // Extract value (use capture group if available, otherwise use full match)
      const value = match[1] || match[0];
      
      results.push({
        type,
        name: rule.name,
        sensitivity: rule.sensitivity,
        value,
        fullMatch: match[0],
        position: match.index,
        length: match[0].length,
        shouldAsk: rule.autoAsk && meetsThreshold,
        suggestedEntryName: generateEntryName(rule.suggestedEntryName, results.length)
      });
    }
  }
  
  // Sort by position
  results.sort((a, b) => a.position - b.position);
  
  return results;
}

/**
 * Generate entry name
 */
function generateEntryName(base, index) {
  if (index === 0) {
    return base;
  }
  return `${base}-${index + 1}`;
}

/**
 * Generate detection prompt message
 * @param {Array} detections - Detection results
 * @returns {string} - Prompt message
 */
export function generatePrompt(detections) {
  if (detections.length === 0) {
    return '';
  }
  
  const lines = ['🔍 Sensitive information detected:', ''];
  
  detections.forEach((d, i) => {
    lines.push(`${i + 1}. ${d.name}`);
    lines.push(`   Type: ${d.type}`);
    lines.push(`   Sensitivity: ${d.sensitivity}`);
    lines.push(`   Suggested entry name: ${d.suggestedEntryName}`);
    lines.push('');
  });
  
  lines.push('Save to password manager?');
  lines.push('');
  lines.push('[Save] [Ignore] [Disable Detection]');
  
  return lines.join('\n');
}

/**
 * Suggest entry type based on detection result
 * @param {string} detectionType - Detection type
 * @returns {string} - Suggested entry type (password/token/api_key/secret)
 */
export function suggestEntryType(detectionType) {
  const typeMap = {
    github_token: 'token',
    gitlab_token: 'token',
    aws_key: 'api_key',
    aws_secret: 'secret',
    openai_key: 'api_key',
    aliyun_key: 'api_key',
    password_context: 'password',
    password_context_en: 'password',
    generic_api_key: 'api_key',
    jwt_token: 'token',
    bearer_token: 'token',
    private_key: 'secret',
    connection_string: 'secret'
  };
  
  return typeMap[detectionType] || 'secret';
}

/**
 * Clean detected value (remove prefixes/suffixes)
 * @param {string} value - Original value
 * @param {string} type - Detection type
 * @returns {string} - Cleaned value
 */
export function cleanValue(value, type) {
  switch (type) {
    case 'bearer_token':
      return value.replace(/^bearer\s+/i, '');
    case 'password_context':
    case 'password_context_en':
      return value.replace(/^["']|["']$/g, '');
    case 'generic_api_key':
      return value.replace(/^["']|["']$/g, '');
    default:
      return value;
  }
}

export default {
  detect,
  generatePrompt,
  suggestEntryType,
  cleanValue,
  RULES: DETECTION_RULES
};
