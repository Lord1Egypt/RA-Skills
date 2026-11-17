// Generated design tokens for TypeScript projects.
export type PortraitThemeId = "deep-space-blue" | "emerald-gold" | "warm-gray-orange" | "midnight-purple" | "minimal-black-white" | "sea-salt-cyan" | "earth-brown" | "vitality-lime";
export type PortraitLayoutId = "diagonal-tech" | "executive-split" | "centered-editorial" | "orbit-focus" | "minimal-column" | "fresh-frame" | "earth-bands" | "playful-corner";

export interface PortraitTheme {
  id: PortraitThemeId;
  index: string;
  name: string;
  description: string;
  recommendedFor: readonly string[];
  layout: PortraitLayoutId;
  mode: "light" | "dark";
  sourcePalette: readonly { role: string; name: string; value: string }[];
  semantic: Readonly<Record<string, string>>;
  gradient: string;
  backgroundAsset: string;
  backgroundPng: string;
}

export const portraitThemeKit = {
  "$schema": "./themes.schema.json",
  "name": "portrait-talk-theme-kit",
  "version": "1.1.0",
  "language": "zh-CN",
  "canvas": {
    "width": 1080,
    "height": 1920,
    "ratio": "9:16",
    "safeArea": {
      "left": 72,
      "right": 72,
      "top": 112,
      "bottom": 180
    },
    "subtitleZone": {
      "x": 72,
      "y": 1490,
      "w": 936,
      "h": 180
    }
  },
  "typography": {
    "fontFamily": "PingFang SC, Microsoft YaHei, Noto Sans SC, system-ui, sans-serif",
    "weights": {
      "regular": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700,
      "heavy": 800
    },
    "sizesPx": {
      "eyebrow": 30,
      "title": 76,
      "lead": 34,
      "emphasis": 96,
      "cta": 32,
      "subtitle": 36,
      "footer": 30,
      "meta": 24
    },
    "lineHeights": {
      "tight": 1.12,
      "title": 1.18,
      "body": 1.45
    }
  },
  "shape": {
    "radiusSmall": 16,
    "radiusMedium": 28,
    "radiusLarge": 48,
    "radiusSpeaker": 58
  },
  "themes": [
    {
      "id": "deep-space-blue",
      "index": "01",
      "name": "深空蓝",
      "description": "专业稳重，科技感强",
      "recommendedFor": [
        "数据分析",
        "技术解释",
        "方法论",
        "AI 实战"
      ],
      "layout": "diagonal-tech",
      "mode": "dark",
      "sourcePalette": [
        {
          "role": "base",
          "name": "深空底色",
          "value": "#0B132B"
        },
        {
          "role": "secondary",
          "name": "钴蓝结构色",
          "value": "#1E3A8A"
        },
        {
          "role": "accent",
          "name": "高亮蓝",
          "value": "#60A5FA"
        },
        {
          "role": "neutral",
          "name": "冷灰白",
          "value": "#E2E8F0"
        }
      ],
      "semantic": {
        "canvas": "#0B132B",
        "surface": "#111D36",
        "surfaceMuted": "rgba(17,29,54,0.72)",
        "textPrimary": "#FFFFFF",
        "textSecondary": "#CBD5E1",
        "emphasis": "#60A5FA",
        "accent": "#60A5FA",
        "accentStrong": "#1E3A8A",
        "border": "rgba(96,165,250,0.80)",
        "ctaBackground": "#1E3A8A",
        "ctaText": "#FFFFFF",
        "speakerSurface": "rgba(96,165,250,0.12)",
        "speakerFigure": "rgba(226,232,240,0.36)",
        "shadow": "rgba(0,0,0,0.42)",
        "glow": "rgba(96,165,250,0.34)"
      },
      "gradient": "linear-gradient(145deg, #0B132B 0%, #081A32 58%, #0B132B 100%)",
      "backgroundAsset": "assets/backgrounds/01-deep-space-blue.svg",
      "backgroundPng": "assets/backgrounds-png/01-deep-space-blue.png"
    },
    {
      "id": "emerald-gold",
      "index": "02",
      "name": "墨绿金",
      "description": "商务高级，信任感强",
      "recommendedFor": [
        "业务复盘",
        "策略分享",
        "经营分析",
        "管理表达"
      ],
      "layout": "executive-split",
      "mode": "dark",
      "sourcePalette": [
        {
          "role": "base",
          "name": "墨绿底色",
          "value": "#0F2E2E"
        },
        {
          "role": "secondary",
          "name": "稳重绿",
          "value": "#1E584E"
        },
        {
          "role": "accent",
          "name": "低饱和金",
          "value": "#D4AF37"
        },
        {
          "role": "neutral",
          "name": "暖米白",
          "value": "#F1EDE3"
        }
      ],
      "semantic": {
        "canvas": "#0F2E2E",
        "surface": "#173A33",
        "surfaceMuted": "rgba(23,58,51,0.76)",
        "textPrimary": "#F8F4E8",
        "textSecondary": "#D6E2DB",
        "emphasis": "#D4AF37",
        "accent": "#D4AF37",
        "accentStrong": "#1E584E",
        "border": "rgba(212,175,55,0.72)",
        "ctaBackground": "#D4AF37",
        "ctaText": "#14241F",
        "speakerSurface": "rgba(212,175,55,0.10)",
        "speakerFigure": "rgba(241,237,227,0.28)",
        "shadow": "rgba(0,0,0,0.38)",
        "glow": "rgba(212,175,55,0.25)"
      },
      "gradient": "linear-gradient(145deg, #0F2E2E 0%, #143B33 56%, #0B2524 100%)",
      "backgroundAsset": "assets/backgrounds/02-emerald-gold.svg",
      "backgroundPng": "assets/backgrounds-png/02-emerald-gold.png"
    },
    {
      "id": "warm-gray-orange",
      "index": "03",
      "name": "暖灰橙",
      "description": "温暖亲和，行动力强",
      "recommendedFor": [
        "干货分享",
        "日常内容",
        "门店培训",
        "用户故事"
      ],
      "layout": "centered-editorial",
      "mode": "light",
      "sourcePalette": [
        {
          "role": "base",
          "name": "暖灰底色",
          "value": "#F7F4F1"
        },
        {
          "role": "accent",
          "name": "行动橙",
          "value": "#FF6A3D"
        },
        {
          "role": "secondary",
          "name": "柔和杏色",
          "value": "#F2B26C"
        },
        {
          "role": "neutral",
          "name": "炭灰文字",
          "value": "#333333"
        }
      ],
      "semantic": {
        "canvas": "#F7F4F1",
        "surface": "#FFFFFF",
        "surfaceMuted": "rgba(255,255,255,0.76)",
        "textPrimary": "#333333",
        "textSecondary": "#4E4540",
        "emphasis": "#C93411",
        "accent": "#FF6A3D",
        "accentStrong": "#C93411",
        "border": "rgba(242,178,108,0.84)",
        "ctaBackground": "#FF6A3D",
        "ctaText": "#000000",
        "speakerSurface": "rgba(51,51,51,0.055)",
        "speakerFigure": "rgba(51,51,51,0.18)",
        "shadow": "rgba(91,67,51,0.16)",
        "glow": "rgba(255,106,61,0.18)"
      },
      "gradient": "linear-gradient(145deg, #FFFFFF 0%, #F7F4F1 60%, #FFF8EF 100%)",
      "backgroundAsset": "assets/backgrounds/03-warm-gray-orange.svg",
      "backgroundPng": "assets/backgrounds-png/03-warm-gray-orange.png"
    },
    {
      "id": "midnight-purple",
      "index": "04",
      "name": "午夜紫",
      "description": "神秘高端，差异化强",
      "recommendedFor": [
        "趋势洞察",
        "创新话题",
        "未来想象",
        "产品发布"
      ],
      "layout": "orbit-focus",
      "mode": "dark",
      "sourcePalette": [
        {
          "role": "base",
          "name": "午夜底色",
          "value": "#1A1026"
        },
        {
          "role": "secondary",
          "name": "高饱和紫",
          "value": "#6D28D9"
        },
        {
          "role": "accent",
          "name": "柔亮紫",
          "value": "#A78BFA"
        },
        {
          "role": "neutral",
          "name": "雾紫白",
          "value": "#EDE9FE"
        }
      ],
      "semantic": {
        "canvas": "#1A1026",
        "surface": "#241536",
        "surfaceMuted": "rgba(36,21,54,0.76)",
        "textPrimary": "#FFFFFF",
        "textSecondary": "#DDD1F3",
        "emphasis": "#A78BFA",
        "accent": "#A78BFA",
        "accentStrong": "#6D28D9",
        "border": "rgba(167,139,250,0.72)",
        "ctaBackground": "#6D28D9",
        "ctaText": "#FFFFFF",
        "speakerSurface": "rgba(167,139,250,0.10)",
        "speakerFigure": "rgba(237,233,254,0.28)",
        "shadow": "rgba(0,0,0,0.46)",
        "glow": "rgba(109,40,217,0.36)"
      },
      "gradient": "linear-gradient(145deg, #1A1026 0%, #12091E 54%, #25113E 100%)",
      "backgroundAsset": "assets/backgrounds/04-midnight-purple.svg",
      "backgroundPng": "assets/backgrounds-png/04-midnight-purple.png"
    },
    {
      "id": "minimal-black-white",
      "index": "05",
      "name": "极简黑白",
      "description": "极致简洁，信息聚焦",
      "recommendedFor": [
        "知识卡片",
        "观点输出",
        "问答栏目",
        "极简访谈"
      ],
      "layout": "minimal-column",
      "mode": "light",
      "sourcePalette": [
        {
          "role": "base",
          "name": "纯黑",
          "value": "#111111"
        },
        {
          "role": "secondary",
          "name": "深灰",
          "value": "#333333"
        },
        {
          "role": "accent",
          "name": "中灰",
          "value": "#999999"
        },
        {
          "role": "neutral",
          "name": "极浅灰",
          "value": "#F5F5F5"
        }
      ],
      "semantic": {
        "canvas": "#F5F5F5",
        "surface": "#FFFFFF",
        "surfaceMuted": "rgba(255,255,255,0.82)",
        "textPrimary": "#111111",
        "textSecondary": "#4A4A4A",
        "emphasis": "#111111",
        "accent": "#111111",
        "accentStrong": "#333333",
        "border": "rgba(17,17,17,0.76)",
        "ctaBackground": "#111111",
        "ctaText": "#FFFFFF",
        "speakerSurface": "rgba(17,17,17,0.055)",
        "speakerFigure": "rgba(17,17,17,0.16)",
        "shadow": "rgba(0,0,0,0.12)",
        "glow": "rgba(0,0,0,0.08)"
      },
      "gradient": "linear-gradient(145deg, #FFFFFF 0%, #F5F5F5 68%, #EEEEEE 100%)",
      "backgroundAsset": "assets/backgrounds/05-minimal-black-white.svg",
      "backgroundPng": "assets/backgrounds-png/05-minimal-black-white.png"
    },
    {
      "id": "sea-salt-cyan",
      "index": "06",
      "name": "海盐青",
      "description": "清新干净，减压舒适",
      "recommendedFor": [
        "用户运营",
        "会员增长",
        "服务流程",
        "轻量科普"
      ],
      "layout": "fresh-frame",
      "mode": "light",
      "sourcePalette": [
        {
          "role": "base",
          "name": "海盐底色",
          "value": "#E6F4F1"
        },
        {
          "role": "secondary",
          "name": "清透青",
          "value": "#14B8A6"
        },
        {
          "role": "accent",
          "name": "薄荷亮色",
          "value": "#5EEAD4"
        },
        {
          "role": "neutral",
          "name": "深海青",
          "value": "#0F766E"
        }
      ],
      "semantic": {
        "canvas": "#E6F4F1",
        "surface": "#F7FFFD",
        "surfaceMuted": "rgba(247,255,253,0.74)",
        "textPrimary": "#07554F",
        "textSecondary": "#24504C",
        "emphasis": "#0F766E",
        "accent": "#14B8A6",
        "accentStrong": "#0F766E",
        "border": "rgba(20,184,166,0.66)",
        "ctaBackground": "#14B8A6",
        "ctaText": "#000000",
        "speakerSurface": "rgba(20,184,166,0.11)",
        "speakerFigure": "rgba(15,118,110,0.20)",
        "shadow": "rgba(15,118,110,0.14)",
        "glow": "rgba(94,234,212,0.26)"
      },
      "gradient": "linear-gradient(145deg, #F7FFFD 0%, #E6F4F1 60%, #D8F5EF 100%)",
      "backgroundAsset": "assets/backgrounds/06-sea-salt-cyan.svg",
      "backgroundPng": "assets/backgrounds-png/06-sea-salt-cyan.png"
    },
    {
      "id": "earth-brown",
      "index": "07",
      "name": "大地棕",
      "description": "沉稳可靠，质感高级",
      "recommendedFor": [
        "商业思考",
        "案例复盘",
        "品牌故事",
        "管理总结"
      ],
      "layout": "earth-bands",
      "mode": "light",
      "sourcePalette": [
        {
          "role": "base",
          "name": "深咖棕",
          "value": "#3E2C23"
        },
        {
          "role": "secondary",
          "name": "皮革棕",
          "value": "#8B5E34"
        },
        {
          "role": "accent",
          "name": "沙金棕",
          "value": "#D9B38C"
        },
        {
          "role": "neutral",
          "name": "暖砂白",
          "value": "#F6F1E9"
        }
      ],
      "semantic": {
        "canvas": "#F6F1E9",
        "surface": "#EFE2D2",
        "surfaceMuted": "rgba(246,241,233,0.78)",
        "textPrimary": "#3E2C23",
        "textSecondary": "#594234",
        "emphasis": "#8B5E34",
        "accent": "#8B5E34",
        "accentStrong": "#3E2C23",
        "border": "rgba(139,94,52,0.66)",
        "ctaBackground": "#6B3F1F",
        "ctaText": "#FFFFFF",
        "speakerSurface": "rgba(139,94,52,0.10)",
        "speakerFigure": "rgba(62,44,35,0.17)",
        "shadow": "rgba(62,44,35,0.18)",
        "glow": "rgba(217,179,140,0.26)"
      },
      "gradient": "linear-gradient(145deg, #F6F1E9 0%, #EEDCC4 62%, #F6F1E9 100%)",
      "backgroundAsset": "assets/backgrounds/07-earth-brown.svg",
      "backgroundPng": "assets/backgrounds-png/07-earth-brown.png"
    },
    {
      "id": "vitality-lime",
      "index": "08",
      "name": "活力青柠",
      "description": "年轻活力，轻快明亮",
      "recommendedFor": [
        "活动宣导",
        "轻松话题",
        "会员日",
        "上新传播"
      ],
      "layout": "playful-corner",
      "mode": "light",
      "sourcePalette": [
        {
          "role": "base",
          "name": "薄荷白",
          "value": "#ECFDF5"
        },
        {
          "role": "secondary",
          "name": "青柠绿",
          "value": "#84CC16"
        },
        {
          "role": "accent",
          "name": "亮青柠",
          "value": "#A3E635"
        },
        {
          "role": "neutral",
          "name": "行动绿",
          "value": "#16A34A"
        }
      ],
      "semantic": {
        "canvas": "#ECFDF5",
        "surface": "#F7FFE9",
        "surfaceMuted": "rgba(247,255,233,0.78)",
        "textPrimary": "#163300",
        "textSecondary": "#3F5B31",
        "emphasis": "#387A05",
        "accent": "#84CC16",
        "accentStrong": "#16A34A",
        "border": "rgba(132,204,22,0.72)",
        "ctaBackground": "#84CC16",
        "ctaText": "#163300",
        "speakerSurface": "rgba(132,204,22,0.11)",
        "speakerFigure": "rgba(22,163,74,0.18)",
        "shadow": "rgba(56,122,5,0.13)",
        "glow": "rgba(163,230,53,0.28)"
      },
      "gradient": "linear-gradient(145deg, #F8FFE9 0%, #ECFDF5 58%, #F1FFD8 100%)",
      "backgroundAsset": "assets/backgrounds/08-vitality-lime.svg",
      "backgroundPng": "assets/backgrounds-png/08-vitality-lime.png"
    }
  ]
} as const;
export const portraitThemes = portraitThemeKit.themes;
export const portraitThemeById = Object.fromEntries(
  portraitThemes.map((theme) => [theme.id, theme]),
) as Record<PortraitThemeId, PortraitTheme>;
