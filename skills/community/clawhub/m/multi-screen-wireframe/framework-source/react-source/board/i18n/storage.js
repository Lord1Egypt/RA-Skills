import { normalizeLocale } from './detect.js'

export const LOCALE_STORAGE_KEY = 'wf-board-locale'

export function readStoredLocale(storage) {
  try {
    const value = storage?.getItem(LOCALE_STORAGE_KEY)
    return normalizeLocale(value)
  } catch {
    return null
  }
}

export function writeStoredLocale(storage, locale) {
  const normalized = normalizeLocale(locale)
  if (!normalized) return false
  try {
    storage?.setItem(LOCALE_STORAGE_KEY, normalized)
    return true
  } catch {
    return false
  }
}
