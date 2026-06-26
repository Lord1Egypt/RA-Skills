# tokens.json → Tailwind（v3 config + v4 @theme 双版本）

> v3 用 `tailwind.config.js theme.extend` 注入；**v4（2026 主流）改用 CSS 内 `@theme {}` 块** ⭐v4.6。两者从同一 tokens.json 出发。

## v4 适配 ⭐v4.6（推荐，2026 起 Tailwind 默认走这条）

Tailwind v4 不再用 `tailwind.config.js`（仍兼容但非主流），改用 CSS 内 `@theme {}` 声明，token 命名前缀化（`--color-<key>` / `--spacing-<key>` 等）。

### jq 转换（v4）

```bash
jq -r '
  "@import \"tailwindcss\";",
  "",
  "@theme {",
  (.color | to_entries[] | "  --color-\(.key): \(.value);"),
  (.spacing | to_entries[] | "  --spacing-\(.key): \(.value)px;"),
  (.radius | to_entries[] | "  --radius-\(.key): \(if (.value | type) == "number" then "\(.value)px" else .value end);"),
  (.shadow | to_entries[] | "  --shadow-\(.key): \(.value);"),
  (.motion.duration // {} | to_entries[] | "  --duration-\(.key): \(.value)ms;"),
  (.motion.easing // {} | to_entries[] | "  --ease-\(.key): \(.value);"),
  "}"
' tokens/bold-minimal.json > generated/tailwind-v4/bold-minimal.css
```

### v4 输出示例（bold-minimal）

```css
@import "tailwindcss";

@theme {
  --color-ink: oklch(0.18 0 0);
  --color-paper: oklch(0.99 0.005 95);
  --color-accent: oklch(0.66 0.20 28);
  --color-mute: oklch(0.45 0 0);
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 32px;
  --spacing-xl: 64px;
  --spacing-2xl: 128px;
  --radius-sm: 2px;
  --radius-md: 8px;
  --radius-lg: 14px;
  --radius-pill: 999px;
  --shadow-card: 0 4px 16px oklch(0 0 0 / .08);
  --duration-fast: 200ms;
  --duration-normal: 300ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
}
```

### v4 用法（utility class 自动生成）

```html
<h1 class="font-display text-ink leading-none">少即是<em>极致</em></h1>
<p class="text-mute mt-md">承诺一个方向</p>
<a class="bg-ink text-paper rounded-pill px-lg py-md transition-colors duration-fast ease-standard">查看 →</a>
```

`text-ink` / `bg-paper` / `rounded-pill` / `px-lg` / `duration-fast` / `ease-standard` 等 utility 由 Tailwind v4 从 `@theme` 块自动生成，不用配置。

### v4 + oklch 兼容

Tailwind v4 直接支持 oklch；不需要 `@property` polyfill。需要 hex fallback 时（旧浏览器），单独写：

```css
@theme {
  --color-ink: #1a1a1a;  /* fallback */
  --color-ink: oklch(0.18 0 0);
}
```

后写的 oklch 在支持的浏览器优先生效；不支持的退到上一行 hex。

---

## v3 适配（legacy / 既有 Tailwind v3 项目）

> 用 `theme.extend` 注入流派 token，**不要覆盖**默认。

## jq 转换

```bash
jq '{
  theme: {
    extend: {
      colors: .color,
      spacing: (.spacing | with_entries({
        key: .key,
        value: (if (.value | type) == "number" then "\(.value)px" else .value end)
      })),
      borderRadius: (.radius | with_entries({
        key: .key,
        value: (if (.value | type) == "number" then "\(.value)px" else .value end)
      })),
      boxShadow: .shadow,
      transitionDuration: (.motion.duration // {} | with_entries({
        key: .key,
        value: "\(.value)ms"
      })),
      transitionTimingFunction: .motion.easing // {}
    }
  }
}' tokens/bold-minimal.json > generated/tailwind/bold-minimal.tailwind.json
```

## 落地到 tailwind.config.js

```js
import boldMinimal from './generated/tailwind/bold-minimal.tailwind.json' assert { type: 'json' };

export default {
  content: ['./**/*.{html,js,ts,tsx,vue}'],
  theme: {
    extend: {
      ...boldMinimal.theme.extend,
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['"IBM Plex Sans"', 'sans-serif']
      }
    }
  }
};
```

用法：

```html
<h1 class="font-display text-ink leading-none">少即是<em>极致</em></h1>
<p class="text-mute mt-md">承诺一个方向</p>
<a class="bg-ink text-paper rounded-pill px-lg py-md transition-colors duration-fast ease-standard">查看 →</a>
```

`duration-fast` / `ease-standard` 是 v4.5 motion tokens 通过 `transitionDuration` / `transitionTimingFunction` 注入到 Tailwind 后产生的 utility class。

## 红线提醒

- 不要把 token **覆盖** Tailwind 默认色（避免污染团队既有项目）— 只用 `extend`
- `fontFamily` 必须**显式**列入 `extend`（typography 字段是字符串描述，jq 不能直接转换）
- `radius.lg = 14` 不要无脑当全局 radius — 必须搭配多档（红线 #9）

## OKLCH 兼容

Tailwind v3.4+ 直接支持 oklch，无需额外配置。Tailwind v3.3- 需要 `@property` polyfill 或退到 hex fallback：

```bash
# hex fallback 版
jq '{ theme: { extend: { colors: .colorHex } } }' tokens/bold-minimal.json
```
