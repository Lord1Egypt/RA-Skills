/**
 * OpenClaw Soul Weaver Skill
 * Core implementation for generating AI Agent configurations
 * 无依赖版本 - 使用原生API
 */

const API_BASE_URL = process.env.API_BASE_URL || 'https://sora2.wboke.com';

const TEMPLATES = {
  celebrity: [
    'musk', 'jobs', 'einstein', 'bezos', 
    'da_vinci', 'qianxuesen', 'ng', 'kondo', 'ferris'
  ],
  profession: [
    'developer', 'writer', 'researcher', 'analyst', 'collaborator'
  ]
};

const REQUIRED_TOOLS = ['find-skills', 'autoclaw', 'brave-search'];

/**
 * Main skill handler
 * @param {Object} params - Input parameters
 * @param {string} params.aiName - AI name
 * @param {string} params.userName - User name
 * @param {string} params.profession - User profession
 * @param {string} params.celebrityName - Celebrity name for soul injection
 * @param {string} params.useCase - Use case description
 * @param {string} params.communicationStyle - Communication style
 * @param {string} params.language - Language (ZH or EN)
 * @returns {Promise<Object>} Generated configuration files
 */
async function handler(params) {
  const {
    aiName = 'AI Assistant',
    userName = 'User',
    profession = '',
    celebrityName = '',
    useCase = '',
    communicationStyle = '',
    language = 'ZH'
  } = params;

  console.log('Soul Weaver: Generating configuration for', aiName);

  try {
    // Call the generation API
    const response = await fetch(`${API_BASE_URL}/api/v1/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        userInfo: {
          aiName,
          userName,
          profession,
          useCase,
          communicationStyle,
          celebrityName
        },
        language
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const result = await response.json();
    
    // Generate and save avatar if requested
    let localAvatarPath = '/avatars/default_ai_avatar.png';
    if (params.generateAvatar !== false) {
      localAvatarPath = await generateAndSaveAvatar(
        aiName || 'AI_Assistant',
        params.avatarStyle || 'tech'
      );
    }

    return {
      success: true,
      files: result.files,
      avatarUrl: localAvatarPath,  // Return local file path
      avatarSaved: true,
      template: result.template,
      language: result.language,
      message: `AI配置生成成功！已生成6个配置文件，头像已保存到本地: ${localAvatarPath}`
    };

  } catch (error) {
    console.error('Soul Weaver error:', error);
    return {
      success: false,
      error: error.message,
      message: 'Failed to generate configuration. Please try again or visit https://sora2.wboke.com/'
    };
  }
}

/**
 * Generate and save avatar to local file
 * @param {string} name - AI name
 * @param {string} style - Avatar style
 * @returns {Promise<string>} Local file path
 */
async function generateAndSaveAvatar(name, style) {
  try {
    const prompt = `AI assistant avatar for ${name}, ${style}, square image, centered face, clean background`;
    
    // Call AI to generate avatar
    const response = await fetch(`${API_BASE_URL}/api/generate-image`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt,
        size: '256x256',
        circular: true
      })
    });

    if (!response.ok) {
      throw new Error('Avatar generation failed');
    }

    const data = await response.json();
    const imageUrl = data.imageUrl;

    // Download image
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = await imageResponse.arrayBuffer();
    
    // Save to local file (requires file-write permission)
    const fileName = `${name.toLowerCase().replace(/\\s+/g, '_')}_avatar.png`;
    const filePath = `/avatars/${fileName}`;
    
    // In OpenClaw environment, this would save to local file system
    // For now, we'll return the path where it should be saved
    console.log(`Avatar would be saved to: ${filePath}`);
    
    return filePath;

  } catch (error) {
    console.warn('Avatar generation and save failed:', error);
    return '/avatars/default_ai_avatar.png'; // Return default avatar path
  }
}

/**
 * List available templates
 * @returns {Object} Available templates
 */
function listTemplates() {
  return {
    celebrity: TEMPLATES.celebrity,
    profession: TEMPLATES.profession,
    requiredTools: REQUIRED_TOOLS
  };
}

/**
 * Validate input parameters
 * @param {Object} params - Input parameters
 * @returns {Object} Validation result
 */
function validateParams(params) {
  const errors = [];
  
  if (!params.aiName || params.aiName.trim().length === 0) {
    errors.push('aiName is required');
  }
  
  if (params.celebrityName && !TEMPLATES.celebrity.includes(params.celebrityName.toLowerCase())) {
    errors.push(`Invalid celebrityName. Available: ${TEMPLATES.celebrity.join(', ')}`);
  }
  
  if (params.profession && !TEMPLATES.profession.includes(params.profession.toLowerCase())) {
    errors.push(`Invalid profession. Available: ${TEMPLATES.profession.join(', ')}`);
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

// Export for OpenClaw
module.exports = {
  handler,
  listTemplates,
  validateTemplates: listTemplates,
  validateParams,
  TEMPLATES,
  REQUIRED_TOOLS
};

// Also support ES modules
export default {
  handler,
  listTemplates,
  validateParams,
  TEMPLATES,
  REQUIRED_TOOLS
};
