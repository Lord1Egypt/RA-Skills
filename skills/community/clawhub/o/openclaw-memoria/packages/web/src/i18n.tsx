/**
 * i18n minimal, zéro dépendance : un dictionnaire plat par langue + un hook
 * `useT()` qui renvoie `t(clé, vars?)`. La langue est persistée dans
 * localStorage (`memoria.lang`), défaut = français (langue source des libellés).
 * Repli en cascade : langue courante → français → la clé elle-même (jamais vide).
 *
 * Convention de clés : namespace par écran, ex. `nav.dashboard`, `audit.title`.
 * Interpolation : `t('x.y', { n: 3 })` remplace `{n}` dans la valeur.
 */
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react'
import { fr } from './messages/fr'
import { en } from './messages/en'
import { es } from './messages/es'
import { pt } from './messages/pt'
import { de } from './messages/de'

export type Lang = 'fr' | 'en' | 'es' | 'pt' | 'de'
export type Messages = Record<string, string>

/** Langues proposées (ordre = ordre d'affichage dans le sélecteur). */
export const LANGS: Array<{ code: Lang; label: string; flag: string }> = [
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'es', label: 'Español', flag: '🇪🇸' },
  { code: 'pt', label: 'Português', flag: '🇵🇹' },
  { code: 'de', label: 'Deutsch', flag: '🇩🇪' },
]

const CATALOGS: Record<Lang, Messages> = { fr, en, es, pt, de }
const STORAGE_KEY = 'memoria.lang'

function initialLang(): Lang {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved && saved in CATALOGS) return saved as Lang
    const nav = (navigator.language || 'fr').slice(0, 2).toLowerCase()
    if (nav in CATALOGS) return nav as Lang
  } catch {
    /* localStorage indisponible → défaut */
  }
  return 'fr'
}

interface I18nCtx {
  lang: Lang
  setLang: (l: Lang) => void
  t: (key: string, vars?: Record<string, string | number>) => string
}

const Ctx = createContext<I18nCtx | null>(null)

function interpolate(tpl: string, vars?: Record<string, string | number>): string {
  if (!vars) return tpl
  return tpl.replace(/\{(\w+)\}/g, (_, k) => (k in vars ? String(vars[k]) : `{${k}}`))
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initialLang)

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, lang)
    } catch {
      /* ignore */
    }
    document.documentElement.lang = lang
  }, [lang])

  const setLang = useCallback((l: Lang) => setLangState(l), [])

  const t = useCallback(
    (key: string, vars?: Record<string, string | number>): string => {
      const val = CATALOGS[lang][key] ?? CATALOGS.fr[key] ?? key
      return interpolate(val, vars)
    },
    [lang],
  )

  return <Ctx.Provider value={{ lang, setLang, t }}>{children}</Ctx.Provider>
}

export function useT(): I18nCtx {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useT doit être utilisé sous <I18nProvider>')
  return ctx
}
