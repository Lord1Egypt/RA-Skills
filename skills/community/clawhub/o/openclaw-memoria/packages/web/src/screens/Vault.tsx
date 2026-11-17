/**
 * Coffre — les secrets (clés API, mots de passe…) détectés dans les
 * conversations sont automatiquement mis à l'abri : Memoria ne garde qu'une
 * RÉFÉRENCE, la valeur vit dans le coffre du système (Keychain macOS / coffre
 * chiffré). Cet écran montre ce qui est protégé — jamais la valeur.
 */
import { getSecrets } from '../api'
import { ErrorBanner, Spinner, useLoad } from '../components/ui'
import { useT } from '../i18n'

export function Vault() {
  const { t } = useT()
  const { state, reload } = useLoad(getSecrets)

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('vault.title')}</h1>
          <p className="muted">{t('vault.lead')}</p>
        </div>
        <button type="button" className="btn btn-ghost" onClick={reload}>{t('common.refresh')}</button>
      </header>

      <div className="vault-explainer">
        {t('vault.explainer.before')}
        <code>[secret:…]</code>
        {t('vault.explainer.mid')} <strong>{t('vault.explainer.never')}</strong>
        {t('vault.explainer.after')}
      </div>

      {state.status === 'loading' && <Spinner />}
      {state.status === 'error' && <ErrorBanner message={state.message} onRetry={reload} />}
      {state.status === 'ready' && (
        state.data.length === 0 ? (
          <div className="empty-state">
            <p>{t('vault.empty.title')}</p>
            <p className="muted">{t('vault.empty.body')}</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr><th>{t('vault.col.reference')}</th><th>{t('vault.col.type')}</th><th>{t('vault.col.location')}</th><th>{t('vault.col.added')}</th></tr>
            </thead>
            <tbody>
              {state.data.map(s => (
                <tr key={s.name}>
                  <td><code>{s.name}</code></td>
                  <td>{s.service ?? '—'}</td>
                  <td className="muted">{s.location.split(':')[0]}</td>
                  <td className="muted">{new Date(s.created_at).toLocaleDateString('fr-FR')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      )}
    </section>
  )
}
