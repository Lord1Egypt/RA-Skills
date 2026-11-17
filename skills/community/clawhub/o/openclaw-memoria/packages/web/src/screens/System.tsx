/**
 * Système — les couches de Memoria, rendues visibles. Les 24 couches cognitives
 * regroupées par rôle, avec leur compteur LIVE (entités, thèmes, procédures…) :
 * on voit la machine tourner. C'est « le cerveau » de Memoria.
 */
import { getCognitiveStats } from '../api'
import { ErrorBanner, Spinner, useLoad } from '../components/ui'
import { useT } from '../i18n'

interface Layer {
  n: number
  nameKey: string
  descKey: string
  /** Clé de stat live (cognitive_stats) — optionnel. */
  stat?: string
}

const BUCKETS: Array<{ titleKey: string; subtitleKey: string; layers: Layer[] }> = [
  {
    titleKey: 'system.bucket_active_title',
    subtitleKey: 'system.bucket_active_subtitle',
    layers: [
      { n: 1, nameKey: 'system.layer_1_name', descKey: 'system.layer_1_desc', stat: 'facts' },
      { n: 2, nameKey: 'system.layer_2_name', descKey: 'system.layer_2_desc' },
      { n: 3, nameKey: 'system.layer_3_name', descKey: 'system.layer_3_desc' },
      { n: 4, nameKey: 'system.layer_4_name', descKey: 'system.layer_4_desc' },
      { n: 5, nameKey: 'system.layer_5_name', descKey: 'system.layer_5_desc' },
      { n: 6, nameKey: 'system.layer_6_name', descKey: 'system.layer_6_desc', stat: 'procedures' },
      { n: 7, nameKey: 'system.layer_7_name', descKey: 'system.layer_7_desc' },
      { n: 8, nameKey: 'system.layer_8_name', descKey: 'system.layer_8_desc' },
      { n: 9, nameKey: 'system.layer_9_name', descKey: 'system.layer_9_desc' },
      { n: 10, nameKey: 'system.layer_10_name', descKey: 'system.layer_10_desc' },
      { n: 11, nameKey: 'system.layer_11_name', descKey: 'system.layer_11_desc', stat: 'wal_buffer' },
    ],
  },
  {
    titleKey: 'system.bucket_enrichment_title',
    subtitleKey: 'system.bucket_enrichment_subtitle',
    layers: [
      { n: 12, nameKey: 'system.layer_12_name', descKey: 'system.layer_12_desc', stat: 'embeddings' },
      { n: 13, nameKey: 'system.layer_13_name', descKey: 'system.layer_13_desc', stat: 'relations' },
      { n: 14, nameKey: 'system.layer_14_name', descKey: 'system.layer_14_desc', stat: 'topics' },
      { n: 15, nameKey: 'system.layer_15_name', descKey: 'system.layer_15_desc', stat: 'observations' },
      { n: 16, nameKey: 'system.layer_16_name', descKey: 'system.layer_16_desc', stat: 'fact_clusters' },
      { n: 17, nameKey: 'system.layer_17_name', descKey: 'system.layer_17_desc' },
      { n: 18, nameKey: 'system.layer_18_name', descKey: 'system.layer_18_desc', stat: 'revision_proposals' },
    ],
  },
  {
    titleKey: 'system.bucket_optional_title',
    subtitleKey: 'system.bucket_optional_subtitle',
    layers: [
      { n: 19, nameKey: 'system.layer_19_name', descKey: 'system.layer_19_desc', stat: 'self_observations' },
      { n: 20, nameKey: 'system.layer_20_name', descKey: 'system.layer_20_desc' },
      { n: 21, nameKey: 'system.layer_21_name', descKey: 'system.layer_21_desc' },
    ],
  },
  {
    titleKey: 'system.bucket_validation_title',
    subtitleKey: 'system.bucket_validation_subtitle',
    layers: [
      { n: 22, nameKey: 'system.layer_22_name', descKey: 'system.layer_22_desc', stat: 'patterns' },
      { n: 23, nameKey: 'system.layer_23_name', descKey: 'system.layer_23_desc' },
      { n: 24, nameKey: 'system.layer_24_name', descKey: 'system.layer_24_desc' },
    ],
  },
]

export function System() {
  const { t } = useT()
  const { state, reload } = useLoad(getCognitiveStats)

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('system.title')}</h1>
          <p className="muted">{t('system.lead')}</p>
        </div>
        <button type="button" className="btn btn-ghost" onClick={reload}>{t('common.refresh')}</button>
      </header>

      {state.status === 'loading' && <Spinner />}
      {state.status === 'error' && <ErrorBanner message={state.message} onRetry={reload} />}
      {state.status === 'ready' && (
        <div className="system-buckets">
          {BUCKETS.map(bucket => (
            <div key={bucket.titleKey} className="system-bucket">
              <div className="system-bucket-head">
                <h2>{t(bucket.titleKey)}</h2>
                <span className="muted">{t(bucket.subtitleKey)}</span>
              </div>
              <div className="layer-grid">
                {bucket.layers.map(l => {
                  const value = l.stat ? state.data[l.stat] : undefined
                  return (
                    <div key={l.n} className="layer-card">
                      <div className="layer-top">
                        <span className="layer-num">{l.n}</span>
                        <strong>{t(l.nameKey)}</strong>
                        {value !== undefined && value > 0 && <span className="layer-stat">{value.toLocaleString('fr-FR')}</span>}
                      </div>
                      <p className="muted layer-desc">{t(l.descKey)}</p>
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
