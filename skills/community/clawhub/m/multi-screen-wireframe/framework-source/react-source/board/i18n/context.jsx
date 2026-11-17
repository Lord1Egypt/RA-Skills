import { DEFAULT_LOCALE, detectLocale, normalizeLocale } from './detect.js'
import { messages } from './locales.js'
import { readStoredLocale, writeStoredLocale } from './storage.js'

function getStorage() {
  try {
    return typeof window === 'undefined' ? null : window.localStorage
  } catch {
    return null
  }
}

export function createTranslator(locale) {
  const dict = messages[locale] || messages[DEFAULT_LOCALE] || {}
  const fallback = messages[DEFAULT_LOCALE] || {}

  return function t(key, vars) {
    let text = dict[key]
    if (text == null) {
      if (typeof console !== 'undefined') console.warn(`[board-i18n] missing key "${key}" for locale "${locale}"`)
      text = fallback[key]
    }
    if (text == null) {
      if (typeof console !== 'undefined') console.warn(`[board-i18n] missing fallback key "${key}"`)
      return key
    }
    if (!vars) return text
    return String(text).replace(/\{(\w+)\}/g, (match, name) => (
      vars[name] != null ? String(vars[name]) : match
    ))
  }
}

export function resolveLocale() {
  const stored = readStoredLocale(getStorage())
  if (stored) return stored
  return detectLocale(typeof navigator === 'undefined' ? null : navigator)
}

const LocaleContext = React.createContext(null)

export function LocaleProvider({ children }) {
  const [locale, setLocaleState] = React.useState(resolveLocale)

  const setLocale = React.useCallback((next) => {
    const normalized = normalizeLocale(next)
    if (!normalized) return
    writeStoredLocale(getStorage(), normalized)
    setLocaleState(normalized)
  }, [])

  const value = React.useMemo(() => ({
    locale,
    setLocale,
    t: createTranslator(locale),
  }), [locale, setLocale])

  return (
    <LocaleContext.Provider value={value}>
      {children}
    </LocaleContext.Provider>
  )
}

export function useLocale() {
  const context = React.useContext(LocaleContext)
  if (!context) throw new Error('useLocale must be used within LocaleProvider')
  return context
}

export function useT() {
  return useLocale().t
}
