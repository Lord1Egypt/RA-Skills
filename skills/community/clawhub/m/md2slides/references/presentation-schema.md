# Presentation Schema 规范

> 这是连接 AI 分析层和 Web 渲染层的中间数据格式。JSON，人类可读写。

---

## 顶层结构

```typescript
interface PresentationSchema {
  meta: PresentationMeta;    // 元数据
  theme: ThemeConfig;        // 主题配置
  slides: Slide[];           // 幻灯片列表
}
```

---

## PresentationMeta

```typescript
interface PresentationMeta {
  title: string;              // 演示标题
  subtitle?: string;          // 副标题
  speaker: string;            // 演讲者
  speakerRole?: string;       // 演讲者角色
  date: string;               // 日期
  duration?: string;          // 预计时长（如 "约55分钟"）
  targetAudience?: string;    // 目标听众
  version?: string;           // 版本号
}
```

| Frontmatter 字段 | Schema 字段 |
|------------------|-------------|
| `title` | `meta.title` |
| `speaker` | `meta.speaker` |
| `role` | `meta.speakerRole` |
| `created` | `meta.date` |
| `duration` | `meta.duration` |
| `target_audience` | `meta.targetAudience` |
| `version` | `meta.version` |

---

## ThemeConfig

```typescript
interface ThemeConfig {
  name: string;
  colors: {
    background: string;
    foreground: string;
    primary: string;
    secondary: string;
    accent: string;
    muted: string;
    border: string;
    codeBackground: string;
    quoteBackground: string;
  };
  fonts: {
    heading: string;
    body: string;
    code: string;
    quote: string;
  };
  fontSizes: {
    title: string;
    slideTitle: string;
    body: string;
    small: string;
    quote: string;
    dataHighlight: string;
  };
}
```

---

## Slide 类型

```typescript
type Slide =
  | CoverSlide
  | AgendaSlide
  | SectionSlide
  | ContentSlide
  | QuoteSlide
  | TableSlide
  | DiagramSlide
  | ComparisonSlide
  | QASlide
  | EndSlide;

interface SlideBase {
  type: SlideType;
  id: string;
}
```

### 1. CoverSlide -- 封面

```typescript
interface CoverSlide extends SlideBase {
  type: "cover";
}
// 封面直接使用 meta 中的 title/speaker/date，不需要额外数据
```

### 2. AgendaSlide -- 议程

```typescript
interface AgendaSlide extends SlideBase {
  type: "agenda";
  title: string;
  items: AgendaItem[];
}

interface AgendaItem {
  chapter: string;
  title: string;
  duration?: string;
  thesis?: string;
}
```

### 3. SectionSlide -- 章节过渡

```typescript
interface SectionSlide extends SlideBase {
  type: "section";
  chapterNumber: string;
  chapterTitle: string;
  duration?: string;
  thesis?: string;
}
```

### 4. ContentSlide -- 内容页

```typescript
interface ContentSlide extends SlideBase {
  type: "content";
  title: string;
  subtitle?: string;
  thesis?: string;
  bullets?: BulletItem[];
  dataHighlights?: DataHighlight[];
  speakerNotes?: string;
}

interface BulletItem {
  text: string;
  subBullets?: string[];
  emphasis?: "normal" | "strong";
}

interface DataHighlight {
  label: string;
  value: string;
  unit?: string;
}
```

### 5. QuoteSlide -- 金句

```typescript
interface QuoteSlide extends SlideBase {
  type: "quote";
  quote: string;
  source?: string;
  context?: string;
}
```

### 6. TableSlide -- 表格

```typescript
interface TableSlide extends SlideBase {
  type: "table";
  title: string;
  columns: string[];
  rows: string[][];
  caption?: string;
}
```

### 7. DiagramSlide -- 图表（Mermaid）

```typescript
interface DiagramSlide extends SlideBase {
  type: "diagram";
  title: string;
  diagramType: "mermaid" | "image";
  content: string;
  caption?: string;
}
```

### 8. ComparisonSlide -- 对比

```typescript
interface ComparisonSlide extends SlideBase {
  type: "comparison";
  title: string;
  leftSide: ComparisonColumn;
  rightSide: ComparisonColumn;
  verdict?: string;
}

interface ComparisonColumn {
  label: string;
  items: string[];
  accent?: "positive" | "negative" | "neutral";
}
```

### 9. QASlide -- 问答

```typescript
interface QASlide extends SlideBase {
  type: "qa";
  questions: QAItem[];
  isEndQA?: boolean;
}

interface QAItem {
  question: string;
  answerDirection: string;
}
```

### 10. EndSlide -- 结束

```typescript
interface EndSlide extends SlideBase {
  type: "end";
  message?: string;
  contactInfo?: string;
}
```

---

## 完整 JSON 示例

```json
{
  "meta": {
    "title": "AI时代下移动端工程体系与研发范式",
    "speaker": "Sopaco",
    "speakerRole": "移动端平台与架构负责人",
    "date": "2026-05-18",
    "duration": "约55分钟",
    "targetAudience": "技术管理者、架构师",
    "version": "v3.0"
  },
  "theme": {
    "name": "default"
  },
  "slides": [
    { "type": "cover", "id": "slide-cover" },
    {
      "type": "agenda",
      "id": "slide-agenda",
      "title": "分享框架（~55分钟）",
      "items": [
        { "chapter": "0", "title": "破冰：一个场景", "duration": "3min", "thesis": "AI能写代码，但写出来的代码能上生产吗？" },
        { "chapter": "1", "title": "两个误区", "duration": "7min", "thesis": "行业在追逐的指标和工具，恰好是价值密度最低的部分" }
      ]
    },
    {
      "type": "content",
      "id": "slide-scene",
      "title": "破冰：一个真实场景",
      "thesis": "AI能写代码，但在大型移动端工程里，能写不等于能上生产",
      "bullets": [
        { "text": "AI几分钟就能生成Kotlin + Rust Native层代码", "emphasis": "normal" },
        { "text": "但你不知道它会不会破坏3个渠道包的编译", "emphasis": "strong" },
        { "text": "不知道JNI签名和Rust binding是否一致", "emphasis": "normal" },
        { "text": "不知道它在低端机上的内存表现", "emphasis": "normal" }
      ],
      "dataHighlights": [
        { "label": "代码规模", "value": "百万行" },
        { "label": "渠道包", "value": "10+" },
        { "label": "交付形态", "value": "5种" }
      ],
      "speakerNotes": "假设你现在用 AI 给 APP 加一个新功能。AI 很快——几分钟就写好了 Kotlin 代码，甚至还生成了对应的 Rust Native 层调用。看起来很完美。但你敢直接合入主干吗？..."
    },
    { "type": "end", "id": "slide-end", "message": "谢谢 / Q & A" }
  ]
}
```