# 扫描报告格式定义

## scan_report.json 结构

扫描报告是一个 JSON 文件，包含从项目中提取的所有需要本地化的文本条目。

### 顶层结构

```json
{
  "version": "1.0",
  "projectPath": "/path/to/project",
  "sourceLanguage": "zh-CN",
  "scanTime": "2026-04-02T16:00:00Z",
  "summary": {
    "totalFiles": 42,
    "codeFiles": 30,
    "resourceFiles": 12,
    "totalTextEntries": 256,
    "totalImageEntries": 15
  },
  "entries": [
    // TextEntry 数组
  ],
  "imageEntries": [
    // ImageEntry 数组
  ]
}
```

### TextEntry 结构

每个文本条目表示项目中发现的一条需要本地化的文本：

```json
{
  "key": "5bdd7fcaa1ed9eb1918c22820c690473",
  "value": "开始",
  "filePath": "assets/Scene/game.scene",
  "type": "text",
  "line": 0,
  "column": 0,
  "loc": {
    "start": { "line": 0, "column": 0 },
    "end": { "line": 0, "column": 0 }
  },
  "range": [0, 0],
  "context": "button_label",
  "category": "ui",
  "variables": []
}
```

字段说明：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `key` | string | ✅ | 条目唯一标识（MD5 hash） |
| `value` | string | ✅ | 原始文本内容 |
| `filePath` | string | ✅ | 相对于项目根目录的文件路径 |
| `type` | enum | ✅ | 条目类型：`text` / `template` / `concatenation` |
| `line` | number | ✅ | 所在行号（0-indexed） |
| `column` | number | ✅ | 所在列号（0-indexed） |
| `loc` | object | ✅ | 精确位置信息 |
| `range` | [number, number] | ✅ | 字符范围 [start, end] |
| `context` | string | ❌ | 上下文说明（如 button_label, dialog_text） |
| `category` | string | ❌ | 功能分类（ui, battle, tutorial, settings, skill_desc 等） |
| `variables` | string[] | ❌ | 包含的变量名列表（用于拼接字符串） |

### type 取值说明

- **`text`**：纯文本，直接替换即可
  ```json
  { "type": "text", "value": "开始游戏", "variables": [] }
  ```

- **`template`**：模板字符串，包含 `${...}` 变量
  ```json
  { "type": "template", "value": "恭喜 ${name} 获得 ${reward}", "variables": ["name", "reward"] }
  ```

- **`concatenation`**：拼接字符串，需要记录完整的拼接表达式
  ```json
  {
    "type": "concatenation",
    "value": "name + \"达到\" + lv + \"级\"",
    "variables": ["name", "lv"],
    "originalExpression": "name + \"达到\" + lv + \"级\"",
    "extractedTexts": ["达到", "级"]
  }
  ```

### ImageEntry 结构

图片条目表示项目中疑似包含文字的图片资源。**每张图片都必须有 OCR 状态**，无论是否识别到文本：

```json
{
  "key": "img_abc123",
  "filePath": "assets/images/start_btn.png",
  "type": "image",
  "fileSize": 12345,
  "dimensions": { "width": 200, "height": 60 },
  "ocrText": "开始游戏",
  "ocrStatus": "recognized",
  "ocrConfidence": 0.95,
  "category": "ui"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `key` | string | ✅ | 条目唯一标识 |
| `filePath` | string | ✅ | 图片文件相对路径 |
| `type` | string | ✅ | 固定为 `image` |
| `fileSize` | number | ✅ | 文件大小（字节） |
| `dimensions` | object | ❌ | 图片尺寸 |
| `ocrText` | string\|null | ✅ | OCR 识别的文本内容。识别到文本时为字符串，未识别到或未执行 OCR 时为 `null` |
| `ocrStatus` | string | ✅ | OCR 状态：`recognized`（识别到文本）/ `empty`（OCR 完成但未识别到文本）/ `failed`（OCR 失败）/ `pending`（未执行 OCR） |
| `ocrConfidence` | number | ❌ | OCR 识别置信度 |
| `category` | string | ❌ | 功能分类 |

#### ocrStatus 取值说明

- **`recognized`**：OCR 成功识别到文本，`ocrText` 为识别结果
- **`empty`**：OCR 执行成功但该图片未识别到任何文本，`ocrText` 为 `null`（说明图片中不含文字或文字不可识别）
- **`failed`**：OCR 任务执行失败，`ocrText` 为 `null`
- **`pending`**：未执行 OCR（`mcpAvailable` 为 `false` 或 `translateImages` 为 `false`），`ocrText` 为 `null`

## analysis_report.json 结构

分析报告包含对项目的整体理解：

```json
{
  "version": "1.0",
  "projectPath": "/path/to/project",
  "analysisTime": "2026-04-02T16:00:00Z",
  "engine": {
    "name": "cocos-creator",
    "version": "3.8",
    "detected": true,
    "evidence": ["检测到 assets/cc.config.json", "使用 cc.Component 基类"]
  },
  "projectStructure": {
    "srcDirs": ["assets/Scripts/"],
    "sceneDirs": ["assets/Scene/"],
    "resourceDirs": ["assets/images/", "assets/audio/"],
    "configFiles": ["game.json", "project.config.json"]
  },
  "i18nReadiness": {
    "hasExistingI18n": false,
    "existingI18nFramework": null,
    "hardcodedTextCount": 256,
    "templateStringCount": 12,
    "concatenationCount": 8,
    "imageWithTextCount": 15
  },
  "modules": [
    {
      "name": "UI",
      "files": ["assets/Scripts/UIManager.ts", "assets/Scene/main.scene"],
      "textCount": 80,
      "description": "用户界面相关文本"
    },
    {
      "name": "Battle",
      "files": ["assets/Scripts/BattleManager.ts"],
      "textCount": 45,
      "description": "战斗系统文本"
    }
  ],
  "recommendations": [
    "建议使用语言包模式，Cocos Creator 支持 i18n 插件",
    "发现 8 处拼接字符串，建议重构为模板字符串",
    "15 张图片包含文字，需要通过图片翻译处理"
  ]
}
```

## glossary.json 结构

```json
{
  "version": "1.0",
  "sourceLanguage": "zh-CN",
  "targetLanguage": "en",
  "entries": [
    {
      "source": "金币",
      "target": "Gold",
      "context": "游戏内货币",
      "frequency": 23,
      "category": "currency",
      "approved": false
    }
  ]
}
```

## text_translations.json 结构

```json
{
  "version": "1.0",
  "sourceLanguage": "zh-CN",
  "targetLanguage": "en",
  "translations": [
    {
      "key": "5bdd7fcaa1ed9eb1918c22820c690473",
      "source": "开始",
      "target": "Start",
      "filePath": "assets/Scene/game.scene",
      "type": "text",
      "loc": { "start": { "line": 0, "column": 0 }, "end": { "line": 0, "column": 0 } },
      "range": [0, 0],
      "status": "translated"
    },
    {
      "key": "concat_abc123",
      "source": "name + \"达到\" + lv + \"级\"",
      "target": "name + \" reached level \" + lv",
      "filePath": "assets/Scripts/GameManager.ts",
      "type": "concatenation",
      "originalExpression": "name + \"达到\" + lv + \"级\"",
      "translatedExpression": "name + \" reached level \" + lv",
      "loc": { "start": { "line": 64, "column": 10 }, "end": { "line": 64, "column": 45 } },
      "range": [1830, 1865],
      "status": "translated"
    }
  ]
}
```

## image_translations.json 结构

```json
{
  "version": "1.0",
  "sourceLanguage": "zh-CN",
  "targetLanguage": "en",
  "translations": [
    {
      "key": "img_abc123",
      "sourceFile": "assets/images/start_btn.png",
      "targetFile": "i18n/assets/en/start_btn.png",
      "ocrText": "开始游戏",
      "translatedText": "Start Game",
      "status": "completed",
      "method": "mcp_image_translation"
    }
  ]
}
```

## verify_report.json 结构

```json
{
  "version": "1.0",
  "verifyTime": "2026-04-02T17:00:00Z",
  "overall": "pass",
  "checks": {
    "syntaxCheck": {
      "status": "pass",
      "total": 30,
      "passed": 30,
      "failed": 0,
      "details": []
    },
    "glossaryConsistency": {
      "status": "pass",
      "total": 50,
      "consistent": 50,
      "inconsistent": 0,
      "details": []
    },
    "textLengthWarnings": {
      "status": "warning",
      "total": 256,
      "normal": 253,
      "warnings": 3,
      "details": [
        {
          "key": "abc123",
          "source": "开始",
          "target": "Get Started Now",
          "sourceLength": 2,
          "targetLength": 15,
          "growthRate": 6.5,
          "filePath": "assets/Scene/game.scene"
        }
      ]
    },
    "sourceLanguageResidual": {
      "status": "pass",
      "residualCount": 0,
      "details": []
    }
  }
}
```
