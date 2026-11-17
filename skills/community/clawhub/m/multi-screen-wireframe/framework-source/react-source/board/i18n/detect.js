export const SUPPORTED_LOCALES = ['zh-CN', 'zh-TW', 'en']
export const DEFAULT_LOCALE = 'en'

export function normalizeLocale(value) {
  if (!value) return null
  const raw = String(value).trim()
  if (SUPPORTED_LOCALES.includes(raw)) return raw

  const lower = raw.toLowerCase()
  if (lower === 'zh-cn' || lower === 'zh') return 'zh-CN'
  if (lower.startsWith('zh-tw') || lower.startsWith('zh-hk') || lower.startsWith('zh-hant')) return 'zh-TW'
  if (lower.startsWith('zh')) return 'zh-CN'
  if (lower.startsWith('en')) return 'en'
  return null
}

export function detectLocale(navigatorLike = typeof navigator === 'undefined' ? null : navigator) {
  const candidates = [
    navigatorLike?.language,
    ...(navigatorLike?.languages || []),
  ]
  for (const candidate of candidates) {
    const normalized = normalizeLocale(candidate)
    if (normalized) return normalized
  }
  return DEFAULT_LOCALE
}
