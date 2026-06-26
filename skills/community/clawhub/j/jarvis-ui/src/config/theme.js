/**
 * Theme Manager - 全域配色系統
 * 負責管理 CSS 變數和通知模組顏色變更
 */

/**
 * HSL 轉 RGB
 * @param {number} h - Hue (0-360)
 * @param {number} s - Saturation (0-100)
 * @param {number} l - Lightness (0-100)
 * @returns {Object} {r, g, b} (0-255)
 */
function hslToRgb(h, s, l) {
  s /= 100;
  l /= 100;
  const k = n => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  return {
    r: Math.round(255 * f(0)),
    g: Math.round(255 * f(8)),
    b: Math.round(255 * f(4))
  };
}

/**
 * 設定主題色相
 * @param {number} hue - 色相值 (0-360)
 */
export function setThemeHue(hue) {
  const root = document.documentElement;
  
  // 設定 --hue 變數
  root.style.setProperty('--hue', hue);
  
  // 計算 RGB 值供 rgba() 使用
  // --accent-primary: hsl(hue, 100%, 63%)
  const primary = hslToRgb(hue, 100, 63);
  root.style.setProperty('--accent-r', primary.r);
  root.style.setProperty('--accent-g', primary.g);
  root.style.setProperty('--accent-b', primary.b);
  root.style.setProperty('--accent-rgb', `${primary.r}, ${primary.g}, ${primary.b}`);
  
  // --accent-secondary: hsl(hue, 62%, 47%)
  const secondary = hslToRgb(hue, 62, 47);
  root.style.setProperty('--accent-secondary-rgb', `${secondary.r}, ${secondary.g}, ${secondary.b}`);
  
  // --accent-tertiary: hsl(hue, 100%, 84%)
  const tertiary = hslToRgb(hue, 100, 84);
  root.style.setProperty('--accent-tertiary-rgb', `${tertiary.r}, ${tertiary.g}, ${tertiary.b}`);
  
  // 儲存到 localStorage
  localStorage.setItem('jarvis-theme-hue', hue);
  
  // 通知所有模組更新
  window.dispatchEvent(new CustomEvent('theme-change', { 
    detail: { 
      hue,
      primary: { r: primary.r, g: primary.g, b: primary.b },
      secondary: { r: secondary.r, g: secondary.g, b: secondary.b },
      tertiary: { r: tertiary.r, g: tertiary.g, b: tertiary.b }
    } 
  }));
}

/**
 * 取得當前主題色相
 * @returns {number} 色相值
 */
export function getThemeHue() {
  const stored = localStorage.getItem('jarvis-theme-hue');
  return stored ? parseInt(stored, 10) : 5; // 預設紅色
}

/**
 * 取得 accent 顏色（HSL 字串）
 * @returns {string} CSS HSL 值
 */
export function getAccentColor() {
  const style = getComputedStyle(document.documentElement);
  return style.getPropertyValue('--accent-primary').trim();
}

/**
 * 取得 accent 顏色（RGB 字串）
 * @returns {string} "r, g, b" 格式
 */
export function getAccentRGB() {
  const style = getComputedStyle(document.documentElement);
  return style.getPropertyValue('--accent-rgb').trim();
}

/**
 * 取得 accent 顏色（RGB Object）
 * @returns {Object} {r, g, b}
 */
export function getAccentRGBObject() {
  const rgb = getAccentRGB();
  const [r, g, b] = rgb.split(',').map(v => parseInt(v.trim(), 10));
  return { r, g, b };
}

/**
 * 取得 accent 顏色（Hex）
 * @returns {string} #RRGGBB
 */
export function getAccentHex() {
  const { r, g, b } = getAccentRGBObject();
  return `#${[r, g, b].map(v => v.toString(16).padStart(2, '0')).join('')}`;
}

/**
 * 初始化主題系統
 */
export function initTheme() {
  const hue = getThemeHue();
  setThemeHue(hue);
}

// 預設色板
export const THEME_PRESETS = [
  { name: '紅色', emoji: '🔴', hue: 5 },
  { name: '橙色', emoji: '🟠', hue: 30 },
  { name: '綠色', emoji: '🟢', hue: 140 },
  { name: '青色', emoji: '🩵', hue: 180 },
  { name: '藍色', emoji: '🔵', hue: 220 },
  { name: '紫色', emoji: '🟣', hue: 270 }
];
