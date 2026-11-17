/**
 * Revue — souvenirs en attente (mode « revue d'abord » et imports en
 * quarantaine) : approuver = le souvenir devient actif, rejeter = effacé
 * définitivement. Tant qu'un souvenir attend ici, aucun agent ne le voit.
 */
import { useCallback, useEffect, useState } from 'react'
import { ApiError, getReview, reviewDecision, type ReviewItem } from '../api'
import { useT } from '../i18n'

export function Review() {
  const { t } = useT()
  const [items, setItems] = useState<ReviewItem[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const refresh = useCallback(async () => {
    try {
      setItems(await getReview())
      setError(null)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t('review.service_unavailable'))
    }
  }, [t])

  useEffect(() => {
    void refresh()
  }, [refresh])

  const decide = useCallback(
    async (ids: string[], decision: 'approve' | 'reject') => {
      setBusy(true)
      try {
        await reviewDecision(ids, decision)
        await refresh()
      } catch (err) {
        setError(err instanceof ApiError ? err.message : t('review.action_failed'))
      } finally {
        setBusy(false)
      }
    },
    [refresh, t],
  )

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('review.title')}</h1>
          <p className="muted">{t('review.lead')}</p>
        </div>
        {items !== null && items.length > 1 && (
          <div className="review-bulk">
            <button
              type="button"
              className="btn btn-primary"
              disabled={busy}
              onClick={() => void decide(items.map(i => i.id), 'approve')}
            >
              {t('review.approve_all', { count: items.length })}
            </button>
            <button
              type="button"
              className="btn btn-danger"
              disabled={busy}
              onClick={() => {
                if (confirm(t('review.reject_all_confirm', { count: items.length }))) {
                  void decide(items.map(i => i.id), 'reject')
                }
              }}
            >
              {t('review.reject_all')}
            </button>
          </div>
        )}
      </header>

      {error && <div className="error-banner">{error}</div>}

      {items === null ? (
        <div className="spinner-row">
          <span className="spinner" aria-hidden />
          {t('common.loading')}
        </div>
      ) : items.length === 0 ? (
        <div className="empty-state">
          <p>{t('review.empty_title')}</p>
          <p className="muted">{t('review.empty_body')}</p>
        </div>
      ) : (
        <ul className="fact-list">
          {items.map(item => (
            <li key={item.id} className="fact-card">
              <p className="fact-content">{item.content}</p>
              <div className="fact-meta">
                {(item.topics ?? []).map(topic => (
                  <span key={topic} className="badge badge-theme" title={t('review.badge_topic_title')}>{topic}</span>
                ))}
                <span className="badge badge-muted">{item.category}</span>
                <span className="badge badge-muted">
                  {item.source_type === 'capture-review' ? t('review.source_capture') : t('review.source_import')}
                </span>
                <span className="muted">{t('review.confidence', { percent: (item.confidence * 100).toFixed(0) })}</span>
                <span className="fact-actions">
                  <button
                    type="button"
                    className="btn btn-primary"
                    disabled={busy}
                    onClick={() => void decide([item.id], 'approve')}
                  >
                    {t('review.approve')}
                  </button>
                  <button
                    type="button"
                    className="btn btn-danger"
                    disabled={busy}
                    onClick={() => void decide([item.id], 'reject')}
                  >
                    {t('review.reject')}
                  </button>
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
