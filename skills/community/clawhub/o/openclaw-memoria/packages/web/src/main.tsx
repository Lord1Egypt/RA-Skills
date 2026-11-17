import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { adoptTokenFromHash } from './api'
import { App } from './App'
import { I18nProvider } from './i18n'
import './styles.css'

// Adoption du token AVANT le premier rendu : l'URL est nettoyée immédiatement.
adoptTokenFromHash()

const container = document.getElementById('root')
if (!container) throw new Error('memoria-ui : élément #root introuvable dans index.html')

createRoot(container).render(
  <StrictMode>
    <I18nProvider>
      <App />
    </I18nProvider>
  </StrictMode>,
)
