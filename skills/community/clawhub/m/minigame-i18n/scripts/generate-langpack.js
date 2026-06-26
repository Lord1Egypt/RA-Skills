#!/usr/bin/env node
/**
 * 语言包生成脚本 v2.0
 * 
 * 基于 text_translations.json，生成游戏引擎**可直接使用**的语言包文件。
 * 
 * 支持的引擎格式：
 *   - cocos-creator    Cocos Creator i18n 插件方案（TS 嵌套对象 + window.languages 挂载）
 *   - cocos-l10n       Cocos Creator ≥3.6 官方 L10N 方案（PO 文件）
 *   - laya             LayaAir 引擎（JSON key-value + 运行时 i18n 模块）
 *   - egret            Egret 白鹭引擎（TS enum 语言包 + exml 字典）
 *   - unity            Unity Localization（JSON 格式 SharedTableData / TableEntry）
 *   - native           原生微信小游戏（JSON key-value + i18n.js 运行时模块）
 * 
 * 使用方法：
 *   node generate-langpack.js --project <projectRoot> --engine <engine> --target-lang <lang>
 * 
 * 参数：
 *   --project      项目根目录路径
 *   --engine       游戏引擎：cocos-creator | cocos-l10n | laya | egret | unity | native
 *   --target-lang  目标语言代码（如 en、ko、th）
 *   --output-dir   输出目录（默认项目根目录下 i18n/langpack/）
 *   --source-lang  源语言代码（默认 zh-CN）
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ============================================================
// 配置
// ============================================================

const args = parseArgs(process.argv.slice(2));
const PROJECT_ROOT = args.project || process.cwd();
const ENGINE = args.engine || 'native';
const TARGET_LANG = args['target-lang'] || 'en';
const SOURCE_LANG = args['source-lang'] || '';
const OUTPUT_DIR = args['output-dir'] || path.join(PROJECT_ROOT, 'i18n', 'langpack');

const I18N_DIR = path.join(PROJECT_ROOT, 'i18n');
const TRANSLATIONS_FILE = path.join(I18N_DIR, 'text_translations.json');

// ============================================================
// 引擎适配器
// ============================================================

const engineAdapters = {
  /**
   * Cocos Creator i18n 插件方案（适用于 <3.6 或使用 i18n 扩展插件的项目）
   * 
   * 官方文档：https://docs.cocos.com/creator/3.8/manual/zh/advanced-topics/i18n.html
   * 
   * 语言包格式说明：
   * - 语言包为 **TypeScript 文件**，采用嵌套对象结构
   * - 通过 `window.languages` 全局对象注册
   * - 语言 ID **不支持符号**（如 `-`），zh-CN 应写为 zhCN
   * - Key 使用点分隔路径引用，如 `test.main`
   * - 文件存放于 `assets/resources/i18n/` 目录
   * 
   * 运行时使用方式：
   *   import * as i18n from 'db://i18n/LanguageData';
   *   i18n.init('en');
   *   const text = i18n.t('ui.start_game');
   *   i18n.updateSceneRenderers(); // 切换语言后刷新
   * 
   * 输出文件示例：
   *   i18n/langpack/cocos-creator/
   *   ├── en.ts         # 英文语言包
   *   └── zhCN.ts       # 中文语言包（源语言）
   */
  'cocos-creator': {
    generate(translations, targetLang, sourceLanguage) {
      // 将 lang code 转为 Cocos 兼容格式（去掉 -）
      const cocosSourceLang = toCocosLangId(sourceLanguage);
      const cocosTargetLang = toCocosLangId(targetLang);

      // 按文件模块分组，生成嵌套对象结构
      const sourcePack = {};
      const targetPack = {};

      for (const entry of translations) {
        const key = generateI18nKey(entry);
        const groupKey = getGroupKey(entry);

        if (!sourcePack[groupKey]) {
          sourcePack[groupKey] = {};
          targetPack[groupKey] = {};
        }

        if (entry.type === 'text') {
          sourcePack[groupKey][key] = entry.source;
          targetPack[groupKey][key] = entry.target;
        } else if (entry.type === 'template') {
          // 模板字符串：将 ${var} 转换为 {var} 格式（Cocos i18n 插件约定）
          sourcePack[groupKey][key] = entry.source.replace(/\$\{(\w+)\}/g, '{$1}');
          targetPack[groupKey][key] = entry.target.replace(/\$\{(\w+)\}/g, '{$1}');
        } else if (entry.type === 'concatenation') {
          const { sourceTemplate, targetTemplate } = convertConcatToTemplate(entry);
          sourcePack[groupKey][key] = sourceTemplate;
          targetPack[groupKey][key] = targetTemplate;
        }
      }

      const subDir = 'cocos-creator';

      return {
        files: [
          {
            path: path.join(subDir, `${cocosSourceLang}.ts`),
            content: generateCocosI18nTs(sourcePack, cocosSourceLang)
          },
          {
            path: path.join(subDir, `${cocosTargetLang}.ts`),
            content: generateCocosI18nTs(targetPack, cocosTargetLang)
          }
        ],
        integrationGuide: generateCocosI18nGuide(cocosSourceLang, cocosTargetLang, subDir)
      };
    }
  },

  /**
   * Cocos Creator L10N 官方方案（适用于 ≥3.6 版本）
   * 
   * 官方文档：https://docs.cocos.com/creator/3.8/manual/zh/editor/l10n/overview.html
   * 
   * L10N 方案支持 PO/CSV/EXCEL 格式：
   * - PO 文件是国际通用的本地化文件格式
   * - 翻译数据存储在 `{项目}/localization-editor/translate-data/` 目录
   * - 可直接导入到 Cocos Creator 编辑器的 L10N 面板
   * 
   * 运行时使用方式：
   *   import l10n from 'db://localization-editor/core/L10nManager';
   *   console.log(l10n.t('key'));
   *   l10n.changeLanguage('en-US'); // 会重启游戏
   *   l10n.currentLanguage;         // 获取当前语言
   *   l10n.languages;               // 获取所有可用语言
   * 
   * 输出文件：
   *   i18n/langpack/cocos-l10n/
   *   ├── en.po            # 英文 PO 翻译文件
   *   └── translations.csv  # CSV 格式翻译表（可导入 L10N 面板）
   */
  'cocos-l10n': {
    generate(translations, targetLang, sourceLanguage) {
      const subDir = 'cocos-l10n';

      // 生成 PO 文件
      const poContent = generatePoFile(translations, targetLang, sourceLanguage);

      // 生成 CSV 文件（L10N 面板可直接导入）
      const csvContent = generateL10nCsv(translations, targetLang, sourceLanguage);

      return {
        files: [
          {
            path: path.join(subDir, `${targetLang}.po`),
            content: poContent
          },
          {
            path: path.join(subDir, 'translations.csv'),
            content: csvContent
          }
        ],
        integrationGuide: generateCocosL10nGuide(targetLang, subDir)
      };
    }
  },

  /**
   * LayaAir 引擎语言包格式
   * 
   * LayaAir 没有官方 i18n 插件，通用做法：
   * - 使用 JSON key-value 语言包
   * - 运行时通过自定义 i18n 模块加载和切换
   * - 语言包按语言代码命名，存放在 `bin/i18n/` 或 `src/i18n/` 目录
   * 
   * 输出文件：
   *   i18n/langpack/laya/
   *   ├── zh-CN.json     # 中文语言包
   *   ├── en.json         # 英文语言包
   *   └── I18nManager.ts  # i18n 管理器（可直接使用）
   */
  'laya': {
    generate(translations, targetLang, sourceLanguage) {
      const sourcePack = {};
      const targetPack = {};

      for (const entry of translations) {
        const key = generateI18nKey(entry);

        if (entry.type === 'concatenation') {
          const { sourceTemplate, targetTemplate } = convertConcatToTemplate(entry);
          sourcePack[key] = sourceTemplate;
          targetPack[key] = targetTemplate;
        } else if (entry.type === 'template') {
          sourcePack[key] = entry.source.replace(/\$\{(\w+)\}/g, '{$1}');
          targetPack[key] = entry.target.replace(/\$\{(\w+)\}/g, '{$1}');
        } else {
          sourcePack[key] = entry.source;
          targetPack[key] = entry.target;
        }
      }

      const subDir = 'laya';

      return {
        files: [
          {
            path: path.join(subDir, `${sourceLanguage}.json`),
            content: JSON.stringify(sourcePack, null, 2)
          },
          {
            path: path.join(subDir, `${targetLang}.json`),
            content: JSON.stringify(targetPack, null, 2)
          },
          {
            path: path.join(subDir, 'I18nManager.ts'),
            content: generateLayaI18nManager(targetLang, sourceLanguage)
          }
        ],
        integrationGuide: generateLayaI18nGuide(targetLang, sourceLanguage, subDir)
      };
    }
  },

  /**
   * Egret 白鹭引擎语言包格式
   * 
   * Egret 项目的多语言方案通常分两部分：
   * 1. TS 源码中的文本 → 使用 const enum 或 JSON 字典
   * 2. EXML 皮肤中的文本 → 使用 window["_LangExml"] 全局字典 + partAdded 运行时替换
   * 
   * 参考：https://blog.csdn.net/linguifa/article/details/122450661
   * 
   * 输出文件：
   *   i18n/langpack/egret/
   *   ├── Language_en.ts   # TS 源码语言包（key-value 字典）
   *   ├── LangExml_en.ts   # EXML 皮肤语言包（中文→目标语言映射）
   *   └── I18nHelper.ts    # i18n 辅助工具（含 partAdded 拦截逻辑）
   */
  'egret': {
    generate(translations, targetLang, sourceLanguage) {
      const tsEntries = [];    // TS 源码中的翻译
      const exmlEntries = [];  // EXML 中的翻译

      for (const entry of translations) {
        const isExml = entry.filePath && (entry.filePath.endsWith('.exml') || entry.context === 'exml');
        if (isExml) {
          exmlEntries.push(entry);
        } else {
          tsEntries.push(entry);
        }
      }

      const subDir = 'egret';
      const files = [];

      // TS 语言包：key-value JSON 字典
      if (tsEntries.length > 0) {
        const tsPack = {};
        for (const entry of tsEntries) {
          const key = generateI18nKey(entry);
          if (entry.type === 'concatenation') {
            const { targetTemplate } = convertConcatToTemplate(entry);
            tsPack[key] = targetTemplate;
          } else if (entry.type === 'template') {
            tsPack[key] = entry.target.replace(/\$\{(\w+)\}/g, '{$1}');
          } else {
            tsPack[key] = entry.target;
          }
        }

        files.push({
          path: path.join(subDir, `Language_${targetLang}.ts`),
          content: generateEgretLanguageTs(tsPack, targetLang)
        });
      }

      // EXML 语言包：中文原文 → 目标语言映射
      if (exmlEntries.length > 0) {
        const exmlPack = {};
        for (const entry of exmlEntries) {
          exmlPack[entry.source] = entry.target;
        }

        files.push({
          path: path.join(subDir, `LangExml_${targetLang}.ts`),
          content: generateEgretExmlTs(exmlPack, targetLang)
        });
      }

      // 如果没有 EXML 但有翻译，也生成全量 source→target 映射（兼容）
      if (exmlEntries.length === 0) {
        const allMapping = {};
        for (const entry of translations) {
          if (entry.type === 'text') {
            allMapping[entry.source] = entry.target;
          }
        }
        files.push({
          path: path.join(subDir, `LangExml_${targetLang}.ts`),
          content: generateEgretExmlTs(allMapping, targetLang)
        });
      }

      // i18n 辅助工具
      files.push({
        path: path.join(subDir, 'I18nHelper.ts'),
        content: generateEgretI18nHelper(targetLang)
      });

      return {
        files,
        integrationGuide: generateEgretI18nGuide(targetLang, subDir)
      };
    }
  },

  /**
   * Unity Localization 语言包格式
   * 
   * Unity 官方 Localization 包使用 StringTable 管理翻译文本。
   * 对于非编辑器环境下的语言包导入，通常使用 JSON 或 CSV 格式。
   * 
   * 输出文件：
   *   i18n/langpack/unity/
   *   ├── StringTable_en.json   # JSON 格式 StringTable
   *   ├── translations.csv       # CSV 格式（可导入 Unity Localization Table）
   *   └── I18nManager.cs         # C# i18n 管理器辅助脚本
   */
  'unity': {
    generate(translations, targetLang, sourceLanguage) {
      const subDir = 'unity';

      // JSON StringTable 格式
      const tableEntries = {};
      for (const entry of translations) {
        const key = generateI18nKey(entry);
        if (entry.type === 'concatenation') {
          const { targetTemplate } = convertConcatToTemplate(entry);
          tableEntries[key] = targetTemplate;
        } else if (entry.type === 'template') {
          // Unity 使用 {0}, {1} 格式的占位符
          let idx = 0;
          const varMap = {};
          const target = entry.target.replace(/\$\{(\w+)\}/g, (_, v) => {
            if (varMap[v] === undefined) varMap[v] = idx++;
            return `{${varMap[v]}}`;
          });
          tableEntries[key] = target;
        } else {
          tableEntries[key] = entry.target;
        }
      }

      // CSV 格式（可导入 Unity Localization Table）
      const csvLines = ['Key,Id,Source,Target'];
      let id = 1;
      for (const entry of translations) {
        const key = generateI18nKey(entry);
        const source = csvEscapeField(entry.source);
        const target = csvEscapeField(entry.target);
        csvLines.push(`${key},${id++},${source},${target}`);
      }

      return {
        files: [
          {
            path: path.join(subDir, `StringTable_${targetLang}.json`),
            content: JSON.stringify({
              m_TableCollectionName: 'GameStrings',
              m_Locale: targetLang,
              m_Entries: tableEntries
            }, null, 2)
          },
          {
            path: path.join(subDir, 'translations.csv'),
            content: csvLines.join('\n')
          },
          {
            path: path.join(subDir, 'I18nManager.cs'),
            content: generateUnityI18nManager(targetLang, sourceLanguage)
          }
        ],
        integrationGuide: generateUnityI18nGuide(targetLang, subDir)
      };
    }
  },

  /**
   * 原生微信小游戏语言包格式
   * 
   * 不依赖任何游戏引擎，适用于纯 JS/Canvas 或非主流引擎的小游戏。
   * 输出简单的 JSON key-value 语言包和一个独立的 i18n 运行时模块。
   * 
   * 输出文件：
   *   i18n/langpack/native/
   *   ├── zh-CN.json   # 中文语言包
   *   ├── en.json       # 英文语言包
   *   └── i18n.js       # 独立 i18n 运行时模块（含使用说明）
   */
  'native': {
    generate(translations, targetLang, sourceLanguage) {
      const sourcePack = {};
      const targetPack = {};

      for (const entry of translations) {
        const key = generateI18nKey(entry);

        if (entry.type === 'concatenation') {
          const { sourceTemplate, targetTemplate } = convertConcatToTemplate(entry);
          sourcePack[key] = sourceTemplate;
          targetPack[key] = targetTemplate;
        } else if (entry.type === 'template') {
          sourcePack[key] = entry.source.replace(/\$\{(\w+)\}/g, '{$1}');
          targetPack[key] = entry.target.replace(/\$\{(\w+)\}/g, '{$1}');
        } else {
          sourcePack[key] = entry.source;
          targetPack[key] = entry.target;
        }
      }

      const subDir = 'native';

      return {
        files: [
          {
            path: path.join(subDir, `${sourceLanguage}.json`),
            content: JSON.stringify(sourcePack, null, 2)
          },
          {
            path: path.join(subDir, `${targetLang}.json`),
            content: JSON.stringify(targetPack, null, 2)
          },
          {
            path: path.join(subDir, 'i18n.js'),
            content: generateNativeI18nModule(targetLang, sourceLanguage)
          }
        ],
        integrationGuide: generateNativeI18nGuide(targetLang, sourceLanguage, subDir)
      };
    }
  }
};

// ============================================================
// 主流程
// ============================================================

async function main() {
  console.log('📦 语言包生成工具 v3.0');
  console.log(`   项目路径: ${PROJECT_ROOT}`);
  console.log(`   游戏引擎: ${ENGINE}`);
  console.log(`   目标语言: ${TARGET_LANG}`);
  console.log(`   输出目录: ${OUTPUT_DIR}`);
  console.log('');

  // 1. 读取翻译表
  if (!fs.existsSync(TRANSLATIONS_FILE)) {
    console.error(`❌ 翻译表不存在: ${TRANSLATIONS_FILE}`);
    process.exit(1);
  }
  const translationsData = JSON.parse(fs.readFileSync(TRANSLATIONS_FILE, 'utf8'));
  const { translations } = translationsData;
  const sourceLanguage = SOURCE_LANG || translationsData.sourceLanguage || 'zh-CN';
  console.log(`✅ 读取翻译表: ${translations.length} 条`);
  console.log(`   源语言: ${sourceLanguage}`);

  // 2. 获取引擎适配器
  const adapter = engineAdapters[ENGINE];
  if (!adapter) {
    console.error(`❌ 不支持的引擎: ${ENGINE}`);
    console.error(`   支持的引擎: ${Object.keys(engineAdapters).join(', ')}`);
    process.exit(1);
  }

  // 3. 生成语言包
  const result = adapter.generate(translations, TARGET_LANG, sourceLanguage);

  // 4. 写入语言包文件到 i18n/langpack/ 目录
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  for (const file of result.files) {
    const filePath = path.join(OUTPUT_DIR, file.path);
    const fileDir = path.dirname(filePath);
    fs.mkdirSync(fileDir, { recursive: true });
    fs.writeFileSync(filePath, file.content, 'utf8');
    console.log(`✅ 生成: ${file.path}`);
  }

  // 5. 生成 key_mapping.json —— 供 replace-text.js --mode langpack 使用
  const keyMapping = generateKeyMapping(translations);
  const keyMappingPath = path.join(OUTPUT_DIR, 'key_mapping.json');
  fs.writeFileSync(keyMappingPath, JSON.stringify(keyMapping, null, 2), 'utf8');
  console.log(`✅ 生成 key 映射表: key_mapping.json (${Object.keys(keyMapping.entries).length} 条)`);

  // 6. 自动复制语言包到引擎项目目录（使之可直接使用）
  console.log('');
  console.log('📂 自动部署语言包到项目目录...');
  const deployResult = deployLangpackToProject(result, ENGINE, TARGET_LANG, sourceLanguage);
  if (deployResult.deployed) {
    for (const dp of deployResult.paths) {
      console.log(`   ✅ 已复制: ${dp}`);
    }
  } else {
    console.log(`   ⚠️ 未自动部署: ${deployResult.reason}`);
  }

  // 7. 自动注入 i18n 初始化代码（在项目入口文件中）
  console.log('');
  console.log('🔧 自动注入 i18n 初始化代码...');
  const injectResult = injectI18nInitCode(ENGINE, TARGET_LANG, sourceLanguage);
  if (injectResult.injected) {
    console.log(`   ✅ 已注入到: ${injectResult.file}`);
  } else {
    console.log(`   ⚠️ 未注入: ${injectResult.reason}`);
    console.log(`   请手动在入口文件中添加以下代码：`);
    console.log(`   ${injectResult.code || '（见集成指南）'}`);
  }

  // 8. 输出集成指南
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📋 语言包集成指南：');
  console.log('');

  if (result.integrationGuide) {
    console.log(result.integrationGuide);
  }

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 9. 生成替换指引（参考用）
  generateReplacementGuide(translations, OUTPUT_DIR);

  // 10. 输出统计摘要
  console.log('');
  const stats = { text: 0, template: 0, concatenation: 0 };
  for (const entry of translations) {
    stats[entry.type] = (stats[entry.type] || 0) + 1;
  }
  console.log(`📊 统计: ${translations.length} 条 (纯文本 ${stats.text} / 模板 ${stats.template} / 拼接 ${stats.concatenation})`);
  console.log('');
  console.log('📌 下一步：执行 replace-text.js --mode langpack 将代码中的中文替换为 i18n 调用');
  console.log(`   node scripts/replace-text.js --project ${PROJECT_ROOT} --engine ${ENGINE} --target-lang ${TARGET_LANG} --mode langpack --backup`);
}

// ============================================================
// 工具函数：Key 生成 & 分组
// ============================================================

/**
 * 生成 i18n key
 * 基于文件路径和原始文本生成稳定的 key
 */
function generateI18nKey(entry) {
  if (entry.key && !entry.key.startsWith('concat_') && !entry.key.startsWith('tpl_')) {
    return sanitizeKey(entry.key);
  }
  // 生成可读的 key
  const fileBase = path.basename(entry.filePath, path.extname(entry.filePath));
  const textHash = crypto.createHash('md5').update(entry.source).digest('hex').substring(0, 8);
  return sanitizeKey(`${fileBase}_${textHash}`);
}

/**
 * 清理 key 中不合法的字符
 */
function sanitizeKey(key) {
  return key.replace(/[^a-zA-Z0-9_]/g, '_');
}

/**
 * 获取按模块/文件分组的 group key
 * 用于 Cocos Creator 嵌套对象格式
 */
function getGroupKey(entry) {
  if (!entry.filePath) return 'common';
  const fileBase = path.basename(entry.filePath, path.extname(entry.filePath));
  // 将文件名转换为合法的对象 key
  return sanitizeKey(fileBase.toLowerCase());
}

/**
 * 将语言代码转换为 Cocos Creator 兼容格式
 * Cocos i18n 插件的语言 ID 不支持 `-` 等符号
 * zh-CN → zhCN, en-US → enUS, ko → ko
 */
function toCocosLangId(langCode) {
  return langCode.replace(/-/g, '');
}

// ============================================================
// 工具函数：模板转换
// ============================================================

/**
 * 将拼接字符串转换为模板字符串
 */
function convertConcatToTemplate(entry) {
  const { originalExpression, translatedExpression, variables } = entry;

  let sourceTemplate = originalExpression || entry.source;
  let targetTemplate = translatedExpression || entry.target;

  sourceTemplate = expressionToTemplate(sourceTemplate, variables);
  targetTemplate = expressionToTemplate(targetTemplate, variables);

  return { sourceTemplate, targetTemplate };
}

/**
 * 将 JS 拼接表达式转换为模板格式
 * "你的" + itemName + "已升到" + level + "级" → 你的{itemName}已升到{level}级
 */
function expressionToTemplate(expr, variables) {
  if (!expr) return '';

  let template = '';
  const parts = expr.split(/\s*\+\s*/);

  for (const part of parts) {
    const trimmed = part.trim();

    const stringMatch = trimmed.match(/^["'`](.*?)["'`]$/);
    if (stringMatch) {
      template += stringMatch[1];
    } else if (variables && variables.includes(trimmed)) {
      template += `{${trimmed}}`;
    } else if (trimmed) {
      template += `{${trimmed}}`;
    }
  }

  return template;
}

/**
 * CSV 字段转义
 */
function csvEscapeField(value) {
  if (!value) return '';
  if (value.includes(',') || value.includes('"') || value.includes('\n')) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

// ============================================================
// Cocos Creator i18n 插件方案 生成器
// ============================================================

/**
 * 生成 Cocos Creator i18n 插件格式的 TS 语言包文件
 * 
 * 格式参考官方文档：
 * https://docs.cocos.com/creator/3.8/manual/zh/advanced-topics/i18n.html
 */
function generateCocosI18nTs(packData, langId) {
  const lines = [];
  lines.push('/**');
  lines.push(` * Cocos Creator i18n 语言包 — ${langId}`);
  lines.push(' * ');
  lines.push(' * 使用方式：将此文件复制到 assets/resources/i18n/ 目录');
  lines.push(` * 引用 key 时使用点分隔路径，如 i18n.t('module.key')`);
  lines.push(' */');
  lines.push('');
  lines.push('const win = window as any;');
  lines.push('');
  lines.push('export const languages = {');

  const groups = Object.keys(packData);
  for (let g = 0; g < groups.length; g++) {
    const group = groups[g];
    const entries = packData[group];
    const keys = Object.keys(entries);

    lines.push(`    "${group}": {`);
    for (let k = 0; k < keys.length; k++) {
      const key = keys[k];
      const value = entries[key].replace(/\\/g, '\\\\').replace(/"/g, '\\"');
      const comma = k < keys.length - 1 ? ',' : '';
      lines.push(`        "${key}": "${value}"${comma}`);
    }
    const groupComma = g < groups.length - 1 ? ',' : '';
    lines.push(`    }${groupComma}`);
  }

  lines.push('};');
  lines.push('');
  lines.push('if (!win.languages) {');
  lines.push('    win.languages = {};');
  lines.push('}');
  lines.push('');
  lines.push(`win.languages.${langId} = languages;`);
  lines.push('');

  return lines.join('\n');
}

function generateCocosI18nGuide(sourceLang, targetLang, subDir) {
  return `[Cocos Creator i18n 插件方案]

1. 将 ${subDir}/${sourceLang}.ts 和 ${subDir}/${targetLang}.ts 复制到项目的 assets/resources/i18n/ 目录

2. 安装 i18n 扩展插件：Cocos Creator 菜单 → 扩展 → 商城 → 搜索 "i18n"

3. 在代码中使用：
   import * as i18n from 'db://i18n/LanguageData';
   
   // 初始化语言
   i18n.init('${targetLang}');
   
   // 获取翻译文本（使用"模块.key"点分隔路径）
   const text = i18n.t('module.key');
   
   // 带变量的文本
   const text = i18n.t('module.key', { name: 'Alice' });
   
   // 切换语言后刷新
   i18n.updateSceneRenderers();

4. 在 Label 节点上使用：添加 LocalizedLabel 组件，Key 填入对应路径

⚠️ 注意：语言 ID 不支持 '-' 符号，zh-CN 已转为 ${sourceLang}
⚠️ 修改文本请编辑语言包文件，不要直接修改 Label 的 string 属性`;
}

// ============================================================
// Cocos Creator L10N 方案 生成器
// ============================================================

/**
 * 生成 PO 格式翻译文件
 */
function generatePoFile(translations, targetLang, sourceLanguage) {
  const lines = [];
  lines.push('# Cocos Creator L10N Translation File');
  lines.push(`# Language: ${targetLang}`);
  lines.push(`# Source: ${sourceLanguage}`);
  lines.push(`# Generated by minigame-i18n`);
  lines.push('');
  lines.push('msgid ""');
  lines.push('msgstr ""');
  lines.push(`"Language: ${targetLang}\\n"`);
  lines.push(`"Content-Type: text/plain; charset=UTF-8\\n"`);
  lines.push(`"Content-Transfer-Encoding: 8bit\\n"`);
  lines.push('');

  for (const entry of translations) {
    const source = entry.source.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
    const target = entry.target.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
    const key = generateI18nKey(entry);

    lines.push(`#. ${entry.filePath || 'unknown'}:${entry.line || 0}`);
    lines.push(`msgctxt "${key}"`);
    lines.push(`msgid "${source}"`);
    lines.push(`msgstr "${target}"`);
    lines.push('');
  }

  return lines.join('\n');
}

/**
 * 生成 CSV 格式翻译表（可导入 L10N 面板）
 */
function generateL10nCsv(translations, targetLang, sourceLanguage) {
  const lines = [];
  lines.push(`Key,${sourceLanguage},${targetLang}`);

  for (const entry of translations) {
    const key = generateI18nKey(entry);
    const source = csvEscapeField(entry.source);
    const target = csvEscapeField(entry.target);
    lines.push(`${key},${source},${target}`);
  }

  return lines.join('\n');
}

function generateCocosL10nGuide(targetLang, subDir) {
  return `[Cocos Creator L10N 官方方案（≥3.6 版本）]

1. PO 文件导入：
   - 打开 Cocos Creator → 面板 → 本地化编辑器
   - 启用 L10N 功能
   - 导入 ${subDir}/${targetLang}.po 文件

2. CSV 文件导入：
   - 将 ${subDir}/translations.csv 导入到 L10N 面板
   - 或复制到 {项目}/localization-editor/translate-data/ 目录

3. 在代码中使用：
   import l10n from 'db://localization-editor/core/L10nManager';
   
   // 获取翻译文本
   const text = l10n.t('key');
   
   // 切换语言（⚠️ 会重启游戏，请先保存数据）
   l10n.changeLanguage('${targetLang}');
   
   // 获取当前语言
   console.log(l10n.currentLanguage);
   
   // 获取所有可用语言
   console.log(l10n.languages);

4. 在 Label 节点上使用：添加 L10nLabel 组件

5. 发布时在构建面板选择目标语言`;
}

// ============================================================
// LayaAir 引擎 生成器
// ============================================================

/**
 * 生成 Laya i18n 管理器 TypeScript 文件
 */
function generateLayaI18nManager(targetLang, sourceLang) {
  return `/**
 * LayaAir i18n 国际化管理器
 * 
 * 使用方法：
 *   import { I18nManager } from './I18nManager';
 *   
 *   // 初始化（在游戏入口处调用一次）
 *   await I18nManager.init('${targetLang}');
 *   
 *   // 获取翻译文本
 *   I18nManager.t('key');
 *   
 *   // 带变量
 *   I18nManager.t('key', { name: 'Alice', level: 10 });
 *   
 *   // 切换语言
 *   await I18nManager.setLanguage('${sourceLang}');
 */

export class I18nManager {
    private static langPacks: Record<string, Record<string, string>> = {};
    private static currentLang: string = '${targetLang}';

    /**
     * 初始化 i18n，加载指定语言包
     * 默认语言为目标语言（${targetLang}），源语言（${sourceLang}）作为回退
     */
    static async init(lang: string = '${targetLang}'): Promise<void> {
        await this.loadLanguage('${sourceLang}');
        await this.loadLanguage(lang);
        this.currentLang = lang;
    }

    /**
     * 加载语言包 JSON 文件
     * 将语言包 JSON 文件放在 bin/i18n/ 或 src/i18n/ 目录下
     */
    static async loadLanguage(lang: string): Promise<boolean> {
        if (this.langPacks[lang]) return true;
        try {
            // LayaAir 资源加载方式（根据项目配置调整路径）
            const response = await fetch(\`i18n/\${lang}.json\`);
            if (response.ok) {
                this.langPacks[lang] = await response.json();
                return true;
            }
        } catch (e) {
            console.warn(\`[i18n] 加载语言包失败: \${lang}\`, e);
        }
        return false;
    }

    /**
     * 设置当前语言
     */
    static async setLanguage(lang: string): Promise<boolean> {
        if (await this.loadLanguage(lang)) {
            this.currentLang = lang;
            return true;
        }
        return false;
    }

    /**
     * 获取当前语言
     */
    static getLanguage(): string {
        return this.currentLang;
    }

    /**
     * 获取翻译文本
     * @param key 翻译 key
     * @param params 变量参数
     */
    static t(key: string, params?: Record<string, any>): string {
        const pack = this.langPacks[this.currentLang];
        if (pack && pack[key]) {
            return this.interpolate(pack[key], params);
        }
        // 回退到源语言
        const fallback = this.langPacks['${sourceLang}'];
        if (fallback && fallback[key]) {
            return this.interpolate(fallback[key], params);
        }
        return key;
    }

    /**
     * 变量插值：将 {name} 替换为 params.name
     */
    private static interpolate(text: string, params?: Record<string, any>): string {
        if (!params) return text;
        return text.replace(/\\{(\\w+)\\}/g, (match, key) => {
            return params[key] !== undefined ? String(params[key]) : match;
        });
    }
}
`;
}

function generateLayaI18nGuide(targetLang, sourceLang, subDir) {
  return `[LayaAir 引擎方案]

1. 将 ${subDir}/${sourceLang}.json 和 ${subDir}/${targetLang}.json 复制到项目中
   建议放在 bin/i18n/ 或 src/i18n/ 目录下

2. 将 ${subDir}/I18nManager.ts 复制到项目的 src/ 目录

3. 在游戏入口处初始化：
   import { I18nManager } from './I18nManager';
   await I18nManager.init('${targetLang}');

4. 在需要翻译的地方使用：
   label.text = I18nManager.t('key');
   label.text = I18nManager.t('key', { name: playerName, level: 10 });

5. 切换语言：
   await I18nManager.setLanguage('${sourceLang}');`;
}

// ============================================================
// Egret 白鹭引擎 生成器
// ============================================================

/**
 * 生成 Egret TS 语言包
 */
function generateEgretLanguageTs(pack, lang) {
  const lines = [];
  lines.push('/**');
  lines.push(` * Egret 语言包 — ${lang}`);
  lines.push(' * ');
  lines.push(` * 使用方式：import { Lang } from './Language_${lang}';`);
  lines.push(` * const text = Lang['key'];`);
  lines.push(' */');
  lines.push('');
  lines.push(`export const Lang: Record<string, string> = {`);

  const keys = Object.keys(pack);
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i];
    const value = pack[key].replace(/\\/g, '\\\\').replace(/"/g, '\\"');
    const comma = i < keys.length - 1 ? ',' : '';
    lines.push(`    "${key}": "${value}"${comma}`);
  }

  lines.push('};');
  lines.push('');
  return lines.join('\n');
}

/**
 * 生成 Egret EXML 语言包（中文→目标语言映射）
 */
function generateEgretExmlTs(mapping, lang) {
  const lines = [];
  lines.push('/**');
  lines.push(` * Egret EXML 皮肤语言包 — ${lang}`);
  lines.push(' * ');
  lines.push(' * 通过 window["_LangExml"] 全局对象注册');
  lines.push(' * 在 eui.Component 的 partAdded 中自动替换 Label/Button 文本');
  lines.push(' */');
  lines.push('');
  lines.push(`(window as any)["_LangExml"] = {`);

  const keys = Object.keys(mapping);
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i].replace(/\\/g, '\\\\').replace(/"/g, '\\"');
    const value = mapping[keys[i]].replace(/\\/g, '\\\\').replace(/"/g, '\\"');
    const comma = i < keys.length - 1 ? ',' : '';
    lines.push(`    "${key}": "${value}"${comma}`);
  }

  lines.push('};');
  lines.push('');
  return lines.join('\n');
}

/**
 * 生成 Egret i18n 辅助工具
 */
function generateEgretI18nHelper(targetLang) {
  return `/**
 * Egret i18n 辅助工具
 * 
 * 功能：
 * 1. 自动拦截 eui.Component.partAdded，替换 EXML 中的文本
 * 2. 提供 i18n.t() 方法用于 TS 代码中的文本翻译
 * 
 * 使用方式：
 *   在游戏入口最前面引入此文件：
 *   import './I18nHelper';
 */

// ============================================================
// partAdded 拦截：自动替换 EXML 皮肤中的文本
// ============================================================
const origPartAdded = eui.Component.prototype['partAdded'];
eui.Component.prototype['partAdded'] = function(partName: string, instance: any): void {
    if (origPartAdded) {
        origPartAdded.call(this, partName, instance);
    }
    const langDict = (window as any)["_LangExml"];
    if (!langDict) return;

    if (instance instanceof eui.Label) {
        const key = instance.text;
        if (langDict.hasOwnProperty(key)) {
            instance.text = langDict[key];
        }
    } else if (instance instanceof eui.Button) {
        const key = instance.label;
        if (langDict.hasOwnProperty(key)) {
            instance.label = langDict[key];
        }
    }
};

// ============================================================
// 修复：为所有含 text 属性的 Label 自动分配 id
// 确保 partAdded 能被调用
// ============================================================
const origAddIds = eui.sys.EXMLParser.prototype['addIds'];
if (origAddIds) {
    eui.sys.EXMLParser.prototype['addIds'] = function(items: any): void {
        if (items) {
            for (let i = 0; i < items.length; i++) {
                const node = items[i];
                if (node.nodeType === 1 && node.attributes &&
                    node.attributes["text"] && !node.attributes["id"]) {
                    if (this.createIdForNode) {
                        this.createIdForNode(node);
                    }
                }
            }
        }
        origAddIds.call(this, items);
    };
}
`;
}

function generateEgretI18nGuide(targetLang, subDir) {
  return `[Egret 白鹭引擎方案]

1. 将 ${subDir}/ 下的文件复制到项目的 src/i18n/ 目录

2. 在游戏入口最前面引入 I18nHelper（拦截 EXML 文本替换）：
   import './i18n/I18nHelper';
   import './i18n/LangExml_${targetLang}';

3. 在 TS 代码中使用语言包字典：
   import { Lang } from './i18n/Language_${targetLang}';
   label.text = Lang['key'];

4. EXML 皮肤中的文本会通过 partAdded 自动替换`;
}

// ============================================================
// Unity 引擎 生成器
// ============================================================

function generateUnityI18nManager(targetLang, sourceLang) {
  return `using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Unity 简易 i18n 管理器
/// 
/// 使用方法：
///   I18nManager.Instance.Init("${targetLang}");
///   string text = I18nManager.Instance.T("key");
///   string text = I18nManager.Instance.T("key", "Alice", 10);
/// </summary>
public class I18nManager : MonoBehaviour
{
    public static I18nManager Instance { get; private set; }

    private Dictionary<string, string> currentPack = new Dictionary<string, string>();
    private Dictionary<string, string> fallbackPack = new Dictionary<string, string>();
    private string currentLang = "${targetLang}";

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    /// <summary>
    /// 初始化语言
    /// </summary>
    public void Init(string lang)
    {
        fallbackPack = LoadLanguagePack("${sourceLang}");
        currentPack = LoadLanguagePack(lang);
        currentLang = lang;
    }

    /// <summary>
    /// 加载语言包 JSON
    /// 将 JSON 文件放在 Resources/I18n/ 目录下
    /// </summary>
    private Dictionary<string, string> LoadLanguagePack(string lang)
    {
        var textAsset = Resources.Load<TextAsset>($"I18n/StringTable_{lang}");
        if (textAsset == null)
        {
            Debug.LogWarning($"[i18n] 语言包不存在: {lang}");
            return new Dictionary<string, string>();
        }
        var data = JsonUtility.FromJson<StringTableData>(textAsset.text);
        return data?.m_Entries ?? new Dictionary<string, string>();
    }

    /// <summary>
    /// 获取翻译文本
    /// </summary>
    public string T(string key, params object[] args)
    {
        string value;
        if (!currentPack.TryGetValue(key, out value))
        {
            if (!fallbackPack.TryGetValue(key, out value))
            {
                return key;
            }
        }
        if (args != null && args.Length > 0)
        {
            value = string.Format(value, args);
        }
        return value;
    }

    /// <summary>
    /// 切换语言
    /// </summary>
    public void SetLanguage(string lang)
    {
        currentPack = LoadLanguagePack(lang);
        currentLang = lang;
    }

    public string CurrentLanguage => currentLang;
}

[System.Serializable]
public class StringTableData
{
    public string m_TableCollectionName;
    public string m_Locale;
    public Dictionary<string, string> m_Entries;
}
`;
}

function generateUnityI18nGuide(targetLang, subDir) {
  return `[Unity 引擎方案]

方案 A：使用 Unity 官方 Localization 包（推荐）
1. Package Manager 安装 com.unity.localization
2. 将 ${subDir}/translations.csv 导入到 String Table
3. 使用 LocalizedString 组件绑定 UI 文本
4. 代码中使用：
   var entry = new LocalizedString("GameStrings", "key");
   string text = entry.GetLocalizedString();

方案 B：使用生成的简易 i18n 管理器
1. 将 ${subDir}/StringTable_${targetLang}.json 复制到 Resources/I18n/ 目录
2. 将 ${subDir}/I18nManager.cs 放到项目 Scripts/ 目录
3. 在场景中创建空 GameObject 挂载 I18nManager 组件
4. 代码中使用：
   I18nManager.Instance.Init("${targetLang}");
   text.text = I18nManager.Instance.T("key");
   text.text = I18nManager.Instance.T("key_with_args", playerName, level);`;
}

// ============================================================
// 原生微信小游戏 生成器
// ============================================================

function generateNativeI18nModule(targetLang, sourceLang) {
  return `/**
 * 小游戏 i18n 国际化模块
 * 
 * 适用于不依赖游戏引擎的纯 JS/Canvas 微信小游戏。
 * 
 * 使用方法：
 *   const i18n = require('./i18n');
 *   i18n.setLanguage('${targetLang}');
 *   
 *   // 纯文本
 *   i18n.t('key');
 *   
 *   // 带变量
 *   i18n.t('key', { name: 'Alice', level: 10 });
 */

const langPacks = {};
let currentLang = '${targetLang}';

/**
 * 加载语言包
 */
function loadLanguage(lang) {
  if (!langPacks[lang]) {
    try {
      const data = require('./' + lang + '.json');
      langPacks[lang] = data;
    } catch (e) {
      console.warn('[i18n] Failed to load language pack: ' + lang);
      return false;
    }
  }
  return true;
}

/**
 * 设置当前语言
 */
function setLanguage(lang) {
  if (loadLanguage(lang)) {
    currentLang = lang;
    return true;
  }
  return false;
}

/**
 * 获取当前语言
 */
function getLanguage() {
  return currentLang;
}

/**
 * 翻译文本
 * @param {string} key - 翻译 key
 * @param {object} params - 变量参数
 * @returns {string} 翻译后的文本
 */
function t(key, params) {
  const pack = langPacks[currentLang];
  if (!pack || !pack[key]) {
    // 回退到源语言
    const fallback = langPacks['${sourceLang}'];
    if (fallback && fallback[key]) {
      return interpolate(fallback[key], params);
    }
    return key; // 返回 key 本身作为最后手段
  }
  return interpolate(pack[key], params);
}

/**
 * 变量插值
 * 将 {name} 替换为 params.name
 */
function interpolate(text, params) {
  if (!params) return text;
  return text.replace(/\\{(\\w+)\\}/g, function(match, key) {
    return params[key] !== undefined ? params[key] : match;
  });
}

// 预加载源语言（作为回退）和目标语言（作为默认）
loadLanguage('${sourceLang}');
loadLanguage('${targetLang}');
currentLang = '${targetLang}';

module.exports = { setLanguage, getLanguage, t, loadLanguage };
`;
}

function generateNativeI18nGuide(targetLang, sourceLang, subDir) {
  return `[原生微信小游戏方案]

1. 将 ${subDir}/ 下的 JSON 和 i18n.js 文件复制到游戏项目中
   建议放在 src/i18n/ 或项目根目录的 i18n/ 下

2. 在游戏入口引入并初始化：
   const i18n = require('./i18n');
   i18n.setLanguage('${targetLang}');

3. 使用翻译文本：
   ctx.fillText(i18n.t('key'), x, y);
   const text = i18n.t('key', { name: playerName });

4. 切换语言：
   i18n.setLanguage('${sourceLang}');`;
}

// ============================================================
// Key 映射表生成（供 replace-text.js --mode langpack 使用）
// ============================================================

/**
 * 生成 key_mapping.json
 * 将 text_translations.json 中每条 entry 的 key/source 映射到 i18n key
 */
function generateKeyMapping(translations) {
  const entries = {};
  for (const entry of translations) {
    const i18nKey = generateI18nKey(entry);
    // 用原始 entry 的 key 和 source 都做映射（双重索引）
    if (entry.key) {
      entries[entry.key] = i18nKey;
    }
    entries[entry.source] = i18nKey;
  }
  return {
    version: '1.0',
    engine: ENGINE,
    generatedAt: new Date().toISOString(),
    entries
  };
}

// ============================================================
// 自动部署语言包到项目目录
// ============================================================

/**
 * 将生成的语言包文件复制到引擎项目对应目录，使之可以直接加载使用
 */
function deployLangpackToProject(result, engine, targetLang, sourceLanguage) {
  const deployPaths = [];

  try {
    switch (engine) {
      case 'cocos-creator': {
        // Cocos Creator i18n 插件：复制到 assets/resources/i18n/
        const targetDir = path.join(PROJECT_ROOT, 'assets', 'resources', 'i18n');
        fs.mkdirSync(targetDir, { recursive: true });
        for (const file of result.files) {
          if (file.path.endsWith('.ts')) {
            const dest = path.join(targetDir, path.basename(file.path));
            fs.writeFileSync(dest, file.content, 'utf8');
            deployPaths.push(path.relative(PROJECT_ROOT, dest));
          }
        }
        return { deployed: deployPaths.length > 0, paths: deployPaths };
      }

      case 'cocos-l10n': {
        // Cocos L10N：复制到 localization-editor/translate-data/
        const targetDir = path.join(PROJECT_ROOT, 'localization-editor', 'translate-data');
        fs.mkdirSync(targetDir, { recursive: true });
        for (const file of result.files) {
          const dest = path.join(targetDir, path.basename(file.path));
          fs.writeFileSync(dest, file.content, 'utf8');
          deployPaths.push(path.relative(PROJECT_ROOT, dest));
        }
        return { deployed: deployPaths.length > 0, paths: deployPaths };
      }

      case 'laya': {
        // Laya：复制到 bin/i18n/ 或 src/i18n/
        const binDir = path.join(PROJECT_ROOT, 'bin', 'i18n');
        const srcDir = path.join(PROJECT_ROOT, 'src', 'i18n');
        // 优先选择已存在的目录
        let targetDir = fs.existsSync(path.join(PROJECT_ROOT, 'bin')) ? binDir : srcDir;
        fs.mkdirSync(targetDir, { recursive: true });
        for (const file of result.files) {
          const dest = path.join(targetDir, path.basename(file.path));
          fs.writeFileSync(dest, file.content, 'utf8');
          deployPaths.push(path.relative(PROJECT_ROOT, dest));
        }
        return { deployed: deployPaths.length > 0, paths: deployPaths };
      }

      case 'egret': {
        // Egret：复制到 src/i18n/
        const targetDir = path.join(PROJECT_ROOT, 'src', 'i18n');
        fs.mkdirSync(targetDir, { recursive: true });
        for (const file of result.files) {
          const dest = path.join(targetDir, path.basename(file.path));
          fs.writeFileSync(dest, file.content, 'utf8');
          deployPaths.push(path.relative(PROJECT_ROOT, dest));
        }
        return { deployed: deployPaths.length > 0, paths: deployPaths };
      }

      case 'unity': {
        // Unity：JSON 复制到 Assets/Resources/I18n/，C# 复制到 Assets/Scripts/I18n/
        const resDir = path.join(PROJECT_ROOT, 'Assets', 'Resources', 'I18n');
        const scriptDir = path.join(PROJECT_ROOT, 'Assets', 'Scripts', 'I18n');
        fs.mkdirSync(resDir, { recursive: true });
        fs.mkdirSync(scriptDir, { recursive: true });
        for (const file of result.files) {
          const basename = path.basename(file.path);
          if (basename.endsWith('.cs')) {
            const dest = path.join(scriptDir, basename);
            fs.writeFileSync(dest, file.content, 'utf8');
            deployPaths.push(path.relative(PROJECT_ROOT, dest));
          } else if (basename.endsWith('.json')) {
            const dest = path.join(resDir, basename);
            fs.writeFileSync(dest, file.content, 'utf8');
            deployPaths.push(path.relative(PROJECT_ROOT, dest));
          } else if (basename.endsWith('.csv')) {
            const dest = path.join(resDir, basename);
            fs.writeFileSync(dest, file.content, 'utf8');
            deployPaths.push(path.relative(PROJECT_ROOT, dest));
          }
        }
        return { deployed: deployPaths.length > 0, paths: deployPaths };
      }

      case 'native': {
        // 原生小游戏：复制到项目根目录的 i18n/ 子目录（运行时 require 可达）
        const targetDir = path.join(PROJECT_ROOT, 'i18n', 'runtime');
        fs.mkdirSync(targetDir, { recursive: true });
        for (const file of result.files) {
          const dest = path.join(targetDir, path.basename(file.path));
          fs.writeFileSync(dest, file.content, 'utf8');
          deployPaths.push(path.relative(PROJECT_ROOT, dest));
        }
        return { deployed: deployPaths.length > 0, paths: deployPaths };
      }

      default:
        return { deployed: false, reason: `未知引擎: ${engine}` };
    }
  } catch (err) {
    return { deployed: false, reason: err.message };
  }
}

// ============================================================
// 自动注入 i18n 初始化代码
// ============================================================

/**
 * 在项目入口文件中注入 i18n 初始化代码
 * 
 * 搜索入口文件的策略：
 *   - Cocos Creator: 查找 assets/scripts 下的 Main.ts 或 GameEntry.ts 等
 *   - Laya: 查找 src/Main.ts 或 bin/js/bundle.js
 *   - Egret: 查找 src/Main.ts
 *   - Unity: 不需要（C# 通过 MonoBehaviour Awake 自初始化）
 *   - Native: 查找 game.js
 */
function injectI18nInitCode(engine, targetLang, sourceLanguage) {
  const initCodeMap = {
    'cocos-creator': {
      importCode: `import * as i18n from 'db://i18n/LanguageData';`,
      initCode: `i18n.init('${toCocosLangId(targetLang)}');`,
      patterns: [
        // Cocos Creator 常见入口文件模式
        'assets/**/Main.ts',
        'assets/**/GameEntry.ts',
        'assets/**/App.ts',
        'assets/**/main.ts',
        'assets/**/GameMain.ts',
      ]
    },
    'cocos-l10n': {
      importCode: `import l10n from 'db://localization-editor/core/L10nManager';`,
      initCode: `// L10N 自动管理语言切换，无需手动 init\n// 如需切换: l10n.changeLanguage('${targetLang}');`,
      patterns: [
        'assets/**/Main.ts',
        'assets/**/GameEntry.ts',
        'assets/**/App.ts',
      ]
    },
    'laya': {
      importCode: `import { I18nManager } from './i18n/I18nManager';`,
      initCode: `await I18nManager.init('${targetLang}');`,
      patterns: [
        'src/Main.ts',
        'src/main.ts',
        'src/GameMain.ts',
      ]
    },
    'egret': {
      importCode: `// i18n 初始化（在 Main.ts 最前面导入）\nimport './i18n/I18nHelper';\nimport './i18n/LangExml_${targetLang}';`,
      initCode: `// Egret i18n 已通过 import 自动初始化`,
      patterns: [
        'src/Main.ts',
        'src/main.ts',
      ]
    },
    'native': {
      importCode: `const i18n = require('./i18n/runtime/i18n');`,
      initCode: `i18n.setLanguage('${targetLang}');`,
      patterns: [
        'game.js',
        'src/game.js',
        'js/game.js',
      ]
    },
    'unity': {
      importCode: null, // Unity C# 不在这里注入
      initCode: null,
      patterns: []
    }
  };

  const config = initCodeMap[engine];
  if (!config || !config.importCode) {
    return { injected: false, reason: `${engine} 引擎不需要或不支持自动注入（Unity 请在场景中挂载 I18nManager 组件）` };
  }

  // 搜索入口文件
  let entryFile = null;
  for (const pattern of config.patterns) {
    const candidates = findFilesByPattern(PROJECT_ROOT, pattern);
    if (candidates.length > 0) {
      entryFile = candidates[0];
      break;
    }
  }

  if (!entryFile) {
    return {
      injected: false,
      reason: `未找到入口文件（搜索模式: ${config.patterns.join(', ')}）`,
      code: `${config.importCode}\n${config.initCode}`
    };
  }

  // 检查是否已注入
  const content = fs.readFileSync(entryFile, 'utf8');
  if (content.includes('i18n') && (content.includes("i18n.init") || content.includes("i18n.setLanguage") || content.includes("I18nManager.init") || content.includes("l10n.changeLanguage") || content.includes("I18nHelper"))) {
    return {
      injected: false,
      reason: `入口文件 ${path.relative(PROJECT_ROOT, entryFile)} 中已有 i18n 相关代码，跳过注入`,
      code: null
    };
  }

  // 注入代码
  try {
    const lines = content.split('\n');
    let insertIdx = 0;

    // 找到合适的插入位置（在已有 import/require 语句之后）
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.startsWith('import ') || line.startsWith('const ') && line.includes('require(') || line.startsWith('//')) {
        insertIdx = i + 1;
      } else if (line !== '' && !line.startsWith('*') && !line.startsWith('/*')) {
        break;
      }
    }

    // 插入 import 和 init 代码
    const injectedCode = `\n// ===== i18n 初始化（由 generate-langpack.js 自动注入）=====\n${config.importCode}\n${config.initCode}\n// ===== i18n 初始化结束 =====\n`;
    lines.splice(insertIdx, 0, injectedCode);

    fs.writeFileSync(entryFile, lines.join('\n'), 'utf8');
    return {
      injected: true,
      file: path.relative(PROJECT_ROOT, entryFile)
    };
  } catch (err) {
    return {
      injected: false,
      reason: `注入失败: ${err.message}`,
      code: `${config.importCode}\n${config.initCode}`
    };
  }
}

/**
 * 简单的文件模式搜索（支持 ** 和 * 通配符）
 */
function findFilesByPattern(baseDir, pattern) {
  const results = [];
  const parts = pattern.split('/');

  function search(dir, partIdx) {
    if (partIdx >= parts.length) return;
    const part = parts[partIdx];
    const isLast = partIdx === parts.length - 1;

    if (part === '**') {
      // 递归搜索所有子目录
      search(dir, partIdx + 1);
      try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
          if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
            search(path.join(dir, entry.name), partIdx);
          }
        }
      } catch (e) {}
      return;
    }

    // 通配符匹配
    const regex = new RegExp('^' + part.replace(/\*/g, '.*').replace(/\?/g, '.') + '$');

    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        if (regex.test(entry.name)) {
          const fullPath = path.join(dir, entry.name);
          if (isLast && entry.isFile()) {
            results.push(fullPath);
          } else if (!isLast && entry.isDirectory()) {
            search(fullPath, partIdx + 1);
          }
        }
      }
    } catch (e) {}
  }

  search(baseDir, 0);
  return results;
}

// ============================================================
// 替换指引（所有引擎通用）—— 已弱化，主要依赖 replace-text.js --mode langpack
// ============================================================

/**
 * 生成替换指引
 * 告诉开发者如何在代码中使用语言包替换硬编码文本
 */
function generateReplacementGuide(translations, outputDir) {
  const guide = [];
  guide.push('# 代码替换指引\n');
  guide.push('以下列出了需要在代码中手动替换的文本位置。\n');
  guide.push('将硬编码的中文文本替换为 `i18n.t("key")` 调用。\n\n');

  // 按文件分组
  const fileGroups = {};
  for (const entry of translations) {
    if (!fileGroups[entry.filePath]) {
      fileGroups[entry.filePath] = [];
    }
    fileGroups[entry.filePath].push(entry);
  }

  for (const [filePath, entries] of Object.entries(fileGroups)) {
    guide.push(`## ${filePath}\n\n`);

    for (const entry of entries) {
      const key = generateI18nKey(entry);

      if (entry.type === 'text') {
        guide.push(`- 行 ${entry.line || '?'}: \`"${entry.source}"\` → \`i18n.t("${key}")\`\n`);
      } else if (entry.type === 'template') {
        const vars = (entry.variables || []).map(v => `${v}: ${v}`).join(', ');
        guide.push(`- 行 ${entry.line || '?'}: \`\`${entry.source}\`\` → \`i18n.t("${key}", { ${vars} })\`\n`);
      } else if (entry.type === 'concatenation') {
        const vars = (entry.variables || []).map(v => `${v}: ${v}`).join(', ');
        guide.push(`- 行 ${entry.line || '?'}: \`${entry.originalExpression || entry.source}\` → \`i18n.t("${key}", { ${vars} })\`\n`);
      }
    }
    guide.push('\n');
  }

  const guidePath = path.join(outputDir, 'replacement_guide.md');
  fs.writeFileSync(guidePath, guide.join(''), 'utf8');
  console.log(`📄 替换指引: ${guidePath}`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].substring(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

// ============================================================
// 执行
// ============================================================

main().catch(err => {
  console.error('❌ 语言包生成失败:', err.message);
  process.exit(1);
});
