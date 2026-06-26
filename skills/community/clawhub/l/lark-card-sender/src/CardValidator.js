/**
 * 卡片验证器
 * Card Validator
 * 
 * @description 验证卡片格式和内容的有效性
 * @author OpenClaw Team
 * @version 1.0.0
 */

class CardValidator {
  constructor(config = {}) {
    this.config = {
      strictMode: false,
      maxTitleLength: 100,
      maxDescriptionLength: 500,
      maxElements: 20,
      ...config
    };
    
    this.validationRules = this.initializeValidationRules();
    
    console.log('🔍 CardValidator initialized');
  }

  /**
   * 初始化验证规则
   */
  initializeValidationRules() {
    return {
      native: {
        required: ['config', 'header', 'elements'],
        optional: ['header.template', 'header.title', 'header.subtitle'],
        rules: {
          'config.wide_screen_mode': (value) => typeof value === 'boolean',
          'header.title.tag': (value) => ['plain_text', 'lark_md'].includes(value),
          'header.title.content': (value) => typeof value === 'string' && value.length > 0,
          'elements': (value) => Array.isArray(value) && value.length > 0,
          'elements.length': (value) => value.length <= this.config.maxElements
        }
      },
      adaptive: {
        required: ['$schema', 'type', 'version', 'body'],
        optional: ['actions'],
        rules: {
          '$schema': (value) => value === 'http://adaptivecards.io/schemas/adaptive-card.json',
          'type': (value) => value === 'AdaptiveCard',
          'version': (value) => ['1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6'].includes(value),
          'body': (value) => Array.isArray(value) && value.length > 0,
          'body.length': (value) => value.length <= this.config.maxElements
        }
      },
      template: {
        required: ['template_id', 'template_variable'],
        optional: [],
        rules: {
          'template_id': (value) => typeof value === 'string' && value.length > 0,
          'template_variable': (value) => typeof value === 'object' && value !== null
        }
      }
    };
  }

  /**
   * 验证卡片
   * @param {Object} cardData - 卡片数据
   * @param {string} format - 格式类型
   * @returns {Object} 验证结果
   */
  validateCard(cardData, format) {
    const result = {
      valid: true,
      errors: [],
      warnings: [],
      format: format
    };

    try {
      // 检查格式是否支持
      if (!this.validationRules[format]) {
        result.valid = false;
        result.errors.push(`不支持的格式: ${format}`);
        return result;
      }

      const rules = this.validationRules[format];
      
      // 检查必需字段
      this.validateRequiredFields(cardData, rules.required, result);
      
      // 检查可选字段
      this.validateOptionalFields(cardData, rules.optional, result);
      
      // 应用特定规则
      this.applyValidationRules(cardData, rules.rules, result);
      
      // 内容验证
      this.validateContent(cardData, format, result);
      
      // 性能验证
      this.validatePerformance(cardData, result);
      
    } catch (error) {
      result.valid = false;
      result.errors.push(`验证过程出错: ${error.message}`);
    }

    return result;
  }

  /**
   * 验证必需字段
   */
  validateRequiredFields(data, requiredFields, result) {
    for (const field of requiredFields) {
      if (!this.hasNestedProperty(data, field)) {
        result.valid = false;
        result.errors.push(`缺少必需字段: ${field}`);
      }
    }
  }

  /**
   * 验证可选字段
   */
  validateOptionalFields(data, optionalFields, result) {
    for (const field of optionalFields) {
      if (this.hasNestedProperty(data, field)) {
        // 如果字段存在，进行基本验证
        const value = this.getNestedProperty(data, field);
        if (value === null || value === undefined || value === '') {
          result.warnings.push(`可选字段为空: ${field}`);
        }
      }
    }
  }

  /**
   * 应用验证规则
   */
  applyValidationRules(data, rules, result) {
    for (const [path, validator] of Object.entries(rules)) {
      if (this.hasNestedProperty(data, path)) {
        const value = this.getNestedProperty(data, path);
        if (!validator(value)) {
          result.valid = false;
          result.errors.push(`字段验证失败: ${path}`);
        }
      }
    }
  }

  /**
   * 验证内容
   */
  validateContent(cardData, format, result) {
    // 验证标题长度
    const title = this.extractTitle(cardData, format);
    if (title && title.length > this.config.maxTitleLength) {
      result.warnings.push(`标题过长 (${title.length}/${this.config.maxTitleLength})`);
    }
    
    // 验证描述长度
    const description = this.extractDescription(cardData, format);
    if (description && description.length > this.config.maxDescriptionLength) {
      result.warnings.push(`描述过长 (${description.length}/${this.config.maxDescriptionLength})`);
    }
    
    // 验证URL格式
    const urls = this.extractUrls(cardData, format);
    for (const url of urls) {
      if (!this.isValidUrl(url)) {
        result.warnings.push(`URL格式可能无效: ${url}`);
      }
    }
    
    // 验证图片URL
    const imageUrls = this.extractImageUrls(cardData, format);
    for (const imageUrl of imageUrls) {
      if (!this.isValidImageUrl(imageUrl)) {
        result.warnings.push(`图片URL格式可能无效: ${imageUrl}`);
      }
    }
  }

  /**
   * 验证性能
   */
  validatePerformance(cardData, result) {
    // 检查卡片大小
    const cardSize = JSON.stringify(cardData).length;
    if (cardSize > 50000) { // 50KB
      result.warnings.push(`卡片数据过大 (${Math.round(cardSize/1024)}KB)，可能影响性能`);
    }
    
    // 检查嵌套深度
    const depth = this.getObjectDepth(cardData);
    if (depth > 10) {
      result.warnings.push(`对象嵌套深度过大 (${depth})，可能影响性能`);
    }
  }

  /**
   * 提取标题
   */
  extractTitle(cardData, format) {
    try {
      switch (format) {
        case 'native':
          return cardData.header?.title?.content;
        case 'adaptive':
          // 查找第一个TextBlock作为标题
          const findTitle = (items) => {
            for (const item of items) {
              if (item.type === 'TextBlock' && item.size === 'Large') {
                return item.text;
              }
              if (item.items) {
                const title = findTitle(item.items);
                if (title) return title;
              }
            }
            return null;
          };
          return findTitle(cardData.body || []);
        case 'template':
          return cardData.template_variable?.title;
        default:
          return null;
      }
    } catch (error) {
      return null;
    }
  }

  /**
   * 提取描述
   */
  extractDescription(cardData, format) {
    try {
      switch (format) {
        case 'native':
          // 查找第一个div元素的文本
          const divElement = cardData.elements?.find(el => el.tag === 'div');
          return divElement?.text?.content;
        case 'adaptive':
          // 查找第二个TextBlock作为描述
          const textBlocks = [];
          const collectTextBlocks = (items) => {
            for (const item of items) {
              if (item.type === 'TextBlock') {
                textBlocks.push(item.text);
              }
              if (item.items) {
                collectTextBlocks(item.items);
              }
            }
          };
          collectTextBlocks(cardData.body || []);
          return textBlocks[1] || textBlocks[0];
        case 'template':
          return cardData.template_variable?.description;
        default:
          return null;
      }
    } catch (error) {
      return null;
    }
  }

  /**
   * 提取URL
   */
  extractUrls(cardData, format) {
    const urls = [];
    
    try {
      const findUrls = (obj) => {
        if (typeof obj === 'object' && obj !== null) {
          for (const key in obj) {
            if (key === 'url' && typeof obj[key] === 'string') {
              urls.push(obj[key]);
            } else if (typeof obj[key] === 'object') {
              findUrls(obj[key]);
            }
          }
        }
      };
      
      findUrls(cardData);
    } catch (error) {
      // 忽略错误
    }
    
    return urls;
  }

  /**
   * 提取图片URL
   */
  extractImageUrls(cardData, format) {
    const imageUrls = [];
    
    try {
      const findImageUrls = (obj) => {
        if (typeof obj === 'object' && obj !== null) {
          for (const key in obj) {
            if ((key === 'url' || key === 'img_key') && this.isImageUrl(obj[key])) {
              imageUrls.push(obj[key]);
            } else if (typeof obj[key] === 'object') {
              findImageUrls(obj[key]);
            }
          }
        }
      };
      
      findImageUrls(cardData);
    } catch (error) {
      // 忽略错误
    }
    
    return imageUrls;
  }

  /**
   * 检查是否有嵌套属性
   */
  hasNestedProperty(obj, path) {
    const keys = path.split('.');
    let current = obj;
    
    for (const key of keys) {
      if (current === null || current === undefined || !current.hasOwnProperty(key)) {
        return false;
      }
      current = current[key];
    }
    
    return true;
  }

  /**
   * 获取嵌套属性
   */
  getNestedProperty(obj, path) {
    const keys = path.split('.');
    let current = obj;
    
    for (const key of keys) {
      if (current === null || current === undefined) {
        return undefined;
      }
      current = current[key];
    }
    
    return current;
  }

  /**
   * 验证URL格式
   */
  isValidUrl(url) {
    if (typeof url !== 'string') return false;
    
    try {
      const urlObj = new URL(url);
      return ['http:', 'https:'].includes(urlObj.protocol);
    } catch {
      return false;
    }
  }

  /**
   * 验证图片URL
   */
  isImageUrl(url) {
    if (typeof url !== 'string') return false;
    
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
    const lowerUrl = url.toLowerCase();
    
    return imageExtensions.some(ext => lowerUrl.includes(ext));
  }

  /**
   * 获取对象深度
   */
  getObjectDepth(obj, depth = 0) {
    if (typeof obj !== 'object' || obj === null) {
      return depth;
    }
    
    let maxDepth = depth;
    for (const key in obj) {
      const currentDepth = this.getObjectDepth(obj[key], depth + 1);
      maxDepth = Math.max(maxDepth, currentDepth);
    }
    
    return maxDepth;
  }

  /**
   * 批量验证
   */
  validateBatch(cardsData, format) {
    const results = [];
    
    for (const cardData of cardsData) {
      results.push(this.validateCard(cardData, format));
    }
    
    return results;
  }

  /**
   * 获取验证规则
   */
  getValidationRules(format) {
    return this.validationRules[format] || null;
  }

  /**
   * 更新验证配置
   */
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
    this.validationRules = this.initializeValidationRules();
  }

  /**
   * 获取版本信息
   */
  getVersion() {
    return {
      version: '1.0.0',
      buildDate: '2026-02-28',
      module: 'CardValidator'
    };
  }
}

module.exports = {
  CardValidator
};