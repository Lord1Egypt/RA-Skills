/**
 * 数据总线 Schema v1.0
 *
 * 定义各技能的输入输出数据格式规范
 * 用于数据验证和技能间数据传递
 *
 * ⭐ v2.8.0 新增
 */

const SCHEMA = {
  /**
   * 环境检查结果
   */
  precheck: {
    required: ['checks', 'summary'],
    optional: ['timestamp'],
    properties: {
      checks: {
        mermaid: { type: 'object' },
        chrome: { type: 'object' },
        python: { type: 'object' },
        dotnet: { type: 'object' }
      },
      summary: {
        passed: { type: 'number' },
        total: { type: 'number' },
        missing: { type: 'array' }
      }
    }
  },

  /**
   * 访谈结果
   */
  interview: {
    required: ['sharedUnderstanding', 'keyDecisions'],
    optional: ['questions', 'designTree'],
    properties: {
      sharedUnderstanding: {
        summary: { type: 'string', required: true },
        productPositioning: { type: 'object' },
        coreFeatures: { type: 'array' },
        complianceRequirements: { type: 'array' },
        technicalConstraints: { type: 'object' },
        businessGoals: { type: 'array' },
        userScenarios: { type: 'array' }
      },
      keyDecisions: {
        type: 'array',
        minItems: 12,
        items: {
          id: { type: 'string', required: true },
          topic: { type: 'string', required: true },
          decision: { type: 'string', required: true },
          rationale: { type: 'string' }
        }
      },
      questions: {
        type: 'array',
        minItems: 16,
        items: {
          question: { type: 'string', required: true },
          answer: { type: 'string' },
          followUp: { type: 'string' }
        }
      },
      designTree: {
        branches: { type: 'array' }
      }
    }
  },

  /**
   * 需求拆解结果
   */
  decomposition: {
    required: ['features', 'userStories'],
    optional: ['moSCoW', 'acceptanceCriteria'],
    properties: {
      features: {
        type: 'array',
        minItems: 1,
        items: {
          id: { type: 'string', required: true },
          name: { type: 'string', required: true },
          description: { type: 'string' },
          priority: { type: 'string', enum: ['P0', 'P1', 'P2', 'P3'] },
          module: { type: 'string' }
        }
      },
      userStories: {
        type: 'array',
        items: {
          id: { type: 'string', required: true },
          asA: { type: 'string', required: true },
          iWant: { type: 'string', required: true },
          soThat: { type: 'string', required: true },
          acceptanceCriteria: { type: 'array' }
        }
      },
      moSCoW: {
        mustHave: { type: 'array' },
        shouldHave: { type: 'array' },
        couldHave: { type: 'array' },
        wontHave: { type: 'array' }
      }
    }
  },

  /**
   * PRD 文档
   */
  prd: {
    required: ['content', 'structure'],
    optional: ['metadata'],
    properties: {
      content: { type: 'string', required: true },
      structure: {
        type: 'array',
        items: {
          level: { type: 'number' },
          title: { type: 'string' },
          id: { type: 'string' }
        }
      },
      metadata: {
        wordCount: { type: 'number' },
        featureCount: { type: 'number' },
        generatedAt: { type: 'string' }
      }
    }
  },

  /**
   * 评审结果
   */
  review: {
    required: ['overall', 'issues'],
    optional: ['scores', 'suggestions'],
    properties: {
      overall: { type: 'number', min: 0, max: 100 },
      issues: {
        type: 'array',
        items: {
          id: { type: 'string' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          category: { type: 'string' },
          description: { type: 'string' },
          location: { type: 'string' },
          suggestion: { type: 'string' }
        }
      },
      scores: {
        completeness: { type: 'number' },
        consistency: { type: 'number' },
        clarity: { type: 'number' },
        compliance: { type: 'number' }
      }
    }
  },

  /**
   * 流程图
   */
  flowchart: {
    required: ['mmdContent'],
    optional: ['pngPath', 'svgPath'],
    properties: {
      mmdContent: { type: 'string', required: true },
      pngPath: { type: 'string' },
      svgPath: { type: 'string' },
      diagramType: { type: 'string', enum: ['flowchart', 'sequence', 'er', 'state', 'gantt'] }
    }
  },

  /**
   * UI/UX 设计
   */
  design: {
    required: ['tokens'],
    optional: ['components', 'pages'],
    properties: {
      tokens: {
        colors: { type: 'object' },
        typography: { type: 'object' },
        spacing: { type: 'array' },
        borderRadius: { type: 'array' },
        shadows: { type: 'array' }
      },
      components: {
        type: 'array',
        items: {
          name: { type: 'string' },
          variants: { type: 'array' },
          states: { type: 'array' }
        }
      }
    }
  },

  /**
   * 原型 v4.0.0
   *
   * 支持多页面原型系统：
   * - sitemap: 页面树结构
   * - routes: 页面间跳转关系
   * - navigation: 导航组件配置
   * - screenshots: 多端截图
   */
  prototype: {
    required: ['sitemap', 'pages'],
    optional: ['routes', 'navigation', 'screenshots', 'prototypeConfig'],
    properties: {
      // 页面树结构
      sitemap: {
        type: 'object',
        properties: {
          pages: {
            type: 'array',
            items: {
              id: { type: 'string', required: true },
              name: { type: 'string', required: true },
              type: { type: 'string', enum: ['list', 'form', 'dashboard', 'detail', 'login', 'landing', 'checkout', 'custom'] },
              parent: { type: 'string' },
              description: { type: 'string' },
              features: { type: 'array' }
            }
          },
          productType: { type: 'string' },
          productName: { type: 'string' }
        }
      },
      // 生成的页面文件
      pages: {
        type: 'array',
        items: {
          id: { type: 'string', required: true },
          name: { type: 'string', required: true },
          htmlPath: { type: 'string', required: true },
          type: { type: 'string' }
        }
      },
      // 路由表
      routes: {
        type: 'array',
        items: {
          from: { type: 'string', required: true },
          to: { type: 'string', required: true },
          trigger: { type: 'string' },
          type: { type: 'string', enum: ['link', 'button', 'tab', 'auto'] }
        }
      },
      // 导航配置
      navigation: {
        type: 'object',
        properties: {
          sidebar: { type: 'object' },
          tabbar: { type: 'object' },
          header: { type: 'object' }
        }
      },
      // 截图
      screenshots: {
        type: 'object',
        properties: {
          desktop: {
            type: 'array',
            items: {
              pageId: { type: 'string' },
              path: { type: 'string' },
              width: { type: 'number' },
              height: { type: 'number' }
            }
          },
          mobile: {
            type: 'array',
            items: {
              pageId: { type: 'string' },
              path: { type: 'string' },
              width: { type: 'number' },
              height: { type: 'number' }
            }
          }
        }
      },
      // 原型配置
      prototypeConfig: {
        type: 'object',
        properties: {
          designTokens: { type: 'object' },
          pageTypesGenerated: { type: 'array' }
        }
      },
      // 兼容旧版本
      htmlPath: { type: 'string' },
      pngPath: { type: 'string' }
    }
  },

  /**
   * 导出结果
   */
  export: {
    required: ['outputPath'],
    optional: ['fileSize', 'imageCount'],
    properties: {
      outputPath: { type: 'string', required: true },
      format: { type: 'string', enum: ['docx', 'pdf'] },
      fileSize: { type: 'number' },
      imageCount: { type: 'number' }
    }
  },

  /**
   * 质量检查结果
   */
  quality: {
    required: ['scores'],
    optional: ['checks', 'docxPath'],
    properties: {
      overall: { type: 'number', min: 0, max: 100 },
      scores: {
        fileIntegrity: { type: 'number' },
        imageEmbedment: { type: 'number' },
        formatConversion: { type: 'number' },
        openXmlValidation: { type: 'number' }
      },
      checks: {
        fileIntegrity: { type: 'object' },
        imagesEmbedment: { type: 'object' },
        formatConversion: { type: 'object' },
        openXmlValidation: { type: 'object' }
      }
    }
  }
};

/**
 * Schema 验证器
 */
class DataBusSchema {
  /**
   * 验证技能输出数据
   *
   * @param {string} skillName - 技能名称
   * @param {object} data - 待验证数据
   * @returns {object} { valid: boolean, errors: string[] }
   */
  validate(skillName, data) {
    const schema = SCHEMA[skillName];
    if (!schema) {
      // 未知技能，跳过验证
      return { valid: true, errors: [], skipped: true };
    }

    const errors = [];

    // 检查必填字段
    if (schema.required) {
      schema.required.forEach(field => {
        if (data[field] === undefined || data[field] === null) {
          errors.push(`缺少必填字段：${field}`);
        }
      });
    }

    // 深度验证（可选）
    if (schema.properties && errors.length === 0) {
      this.validateProperties(skillName, data, schema.properties, '', errors);
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }

  /**
   * 递归验证属性
   */
  validateProperties(skillName, data, properties, path, errors) {
    Object.entries(properties).forEach(([key, propDef]) => {
      const value = data[key];
      const currentPath = path ? `${path}.${key}` : key;

      if (value === undefined || value === null) {
        return; // 已由 required 检查
      }

      // 类型检查
      if (propDef.type) {
        const actualType = Array.isArray(value) ? 'array' : typeof value;
        if (actualType !== propDef.type) {
          errors.push(`${currentPath}: 类型错误，期望 ${propDef.type}，实际 ${actualType}`);
        }
      }

      // 数组检查
      if (propDef.type === 'array' && Array.isArray(value)) {
        // 最小长度
        if (propDef.minItems && value.length < propDef.minItems) {
          errors.push(`${currentPath}: 数组长度不足，期望 ≥${propDef.minItems}，实际 ${value.length}`);
        }

        // 子项验证
        if (propDef.items && value.length > 0) {
          value.forEach((item, index) => {
            if (typeof item === 'object') {
              this.validateProperties(skillName, item, propDef.items, `${currentPath}[${index}]`, errors);
            }
          });
        }
      }

      // 枚举检查
      if (propDef.enum && !propDef.enum.includes(value)) {
        errors.push(`${currentPath}: 值不在允许范围内，允许：${propDef.enum.join(', ')}`);
      }

      // 数字范围检查
      if (typeof value === 'number') {
        if (propDef.min !== undefined && value < propDef.min) {
          errors.push(`${currentPath}: 数值过小，期望 ≥${propDef.min}，实际 ${value}`);
        }
        if (propDef.max !== undefined && value > propDef.max) {
          errors.push(`${currentPath}: 数值过大，期望 ≤${propDef.max}，实际 ${value}`);
        }
      }

      // 嵌套对象验证
      if (typeof value === 'object' && !Array.isArray(value) && propDef.properties) {
        this.validateProperties(skillName, value, propDef.properties, currentPath, errors);
      }
    });
  }

  /**
   * 获取技能 schema
   */
  getSchema(skillName) {
    return SCHEMA[skillName] || null;
  }

  /**
   * 列出所有已定义 schema 的技能
   */
  listDefinedSkills() {
    return Object.keys(SCHEMA);
  }
}

module.exports = { DataBusSchema, SCHEMA };