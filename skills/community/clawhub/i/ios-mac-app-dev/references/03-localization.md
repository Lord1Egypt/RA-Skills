# 国际化与多语言支持

> 50+ 语言全流程支持，基于 Apple 官方国际化框架。

## 核心技术架构

```swift
import SwiftUI

@Observable
class LocalizationManager {
    var currentLocale: Locale
    var availableLanguages: [String]
    
    init() {
        self.availableLanguages = Bundle.main.localizations
        self.currentLocale = Locale.autoupdatingCurrent
    }
    
    func switchToLanguage(_ languageCode: String) {
        UserDefaults.standard.set([languageCode], forKey: "AppleLanguages")
        UserDefaults.standard.synchronize()
        // 需要重启应用生效
    }
}
```

## 本地化检查清单

| 类别 | 检查项 | 实现方式 |
|------|--------|----------|
| 文本 | 所有用户可见文本 | `NSLocalizedString` + `String Catalog` |
| 复数 | 复数形式处理 | `.stringsdict` (如 "1 item" vs "5 items") |
| 日期 | 按区域格式化 | `DateFormatter` |
| 货币 | 区域货币格式 | `NumberFormatter` |
| RTL | RTL语言适配 | `semanticContentAttribute = .forceRightToLeft` |
| 图像 | 避免文化冲突 | 中东地区避免左手图标 |
| 颜色 | 文化禁忌色 | 巴西忌用紫色 |
| 字体 | CJK/阿拉伯字体 | PingFang, Hiragino, 等 |
| 文本长度 | 德语/俄语长文本 | Auto Layout 自适应 |

## 支持语言列表（完整版）

| 语言代码 | 名称 | 地区 |
|----------|------|------|
| en | English | 🇺🇸 美国 |
| zh-Hans | 简体中文 | 🇨🇳 中国 |
| zh-Hant | 繁體中文 | 🇭🇰 香港/台湾 |
| ja | 日本語 | 🇯🇵 日本 |
| ko | 한국어 | 🇰🇷 韩国 |
| fr | Français | 🇫🇷 法国 |
| de | Deutsch | 🇩🇪 德国 |
| es | Español | 🇪🇸 西班牙 |
| ar | العربية | 🇸🇦 沙特 |
| ru | Русский | 🇷🇺 俄罗斯 |
| pt-BR | Português (Brasil) | 🇧🇷 巴西 |
| th | ไทย | 🇹🇭 泰国 |
| vi | Tiếng Việt | 🇻🇳 越南 |
| it | Italiano | 🇮🇹 意大利 |
| nl | Nederlands | 🇳🇱 荷兰 |
| + 更多... | Apple 支持全部 50 种语言 |

## 设备端翻译 (iOS 17.4+)

```swift
import Translation

class OnDeviceTranslator {
    func translateText(_ text: String, 
                       from source: Locale.Language, 
                       to target: Locale.Language) async -> String? {
        guard let session = try? await TranslationSession(
            source: source,
            target: target
        ) else { return nil }
        
        let result = try? await session.translate(text)
        return result?.translatedText
    }
}
```

## String Catalog 模板

```
项目目录/
├── Localizable.xcstrings          # 主字符串目录
├── InfoPlist.xcstrings           # Info.plist 本地化
└── <Feature>.xcstrings            # 按功能拆分
```

**关键规则：** 所有 String Catalog 中的字符串使用英语 key，各语言 region 提供翻译值。复数形式在 `.xcstrings` 中通过 `pluralization` 配置。
