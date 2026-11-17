/**
 * Tableau de bord — l'état de la mémoire en un coup d'œil :
 * santé (doctor), compteurs (stats), souvenirs en attente de traitement (WAL),
 * et ALERTE moteur d'extraction (anti-mort-silencieuse : si aucun moteur n'est
 * disponible, on le dit en rouge, on ne laisse pas la file gonfler en silence).
 */
import { getDoctor, getLlmHealth, getOverview, getStats, type AgentOverview, type DoctorReport, type LlmHealth, type Stats } from '../api'
import { ErrorBanner, Spinner, formatBytes, useLoad } from '../components/ui'
import { useT } from '../i18n'

const AGENT_LABELS: Record<string, string> = {
  'claude-code': 'Claude Code',
  codex: 'Codex',
  openclaw: 'OpenClaw',
}

// Types de base de données connus → clé i18n dashboard.dbKind.<kind> (repli : le kind brut).
const KNOWN_DB_KINDS = new Set(['registry', 'assistant', 'shared'])

export function Dashboard({ onConnect, onConfigure }: { onConnect: () => void; onConfigure?: () => void }) {
  const { t } = useT()
  const { state, reload } = useLoad(async () => {
    const [stats, doctor, overview, llmHealth] = await Promise.all([
      getStats(),
      getDoctor(),
      getOverview().catch(() => []),
      // route « contrat » : absente sur un vieux service → pas de bannière
      getLlmHealth().catch(() => null),
    ])
    return { stats, doctor, overview, llmHealth }
  })

  return (
    <section>
      <header className="screen-head">
        <h1>{t('dashboard.title')}</h1>
        <button type="button" className="btn btn-ghost" onClick={reload}>
          {t('common.refresh')}
        </button>
      </header>

      {state.status === 'loading' && <Spinner />}
      {state.status === 'error' && <ErrorBanner message={state.message} onRetry={reload} />}
      {state.status === 'ready' && (
        <DashboardBody
          stats={state.data.stats}
          doctor={state.data.doctor}
          overview={state.data.overview}
          llmHealth={state.data.llmHealth}
          onConnect={onConnect}
          onConfigure={onConfigure}
        />
      )}
    </section>
  )
}

function DashboardBody({
  stats,
  doctor,
  overview,
  llmHealth,
  onConnect,
  onConfigure,
}: {
  stats: Stats
  doctor: DoctorReport
  overview: AgentOverview[]
  llmHealth: LlmHealth | null
  onConnect: () => void
  onConfigure?: () => void
}) {
  const { t } = useT()
  const walPending = doctor.databases.reduce((sum, db) => sum + (db.wal_pending ?? 0), 0)

  return (
    <>
      <LlmBanner health={llmHealth} onConfigure={onConfigure} />

      <HealthCard doctor={doctor} />

      <div className="stat-grid">
        <StatCard value={stats.facts} label={t('dashboard.stat.factsLabel')} hint={t('dashboard.stat.factsHint')} />
        <StatCard value={stats.instances} label={t('dashboard.stat.agentsLabel')} hint={t('dashboard.stat.agentsHint')} />
        <StatCard value={stats.databases} label={t('dashboard.stat.spacesLabel')} hint={t('dashboard.stat.spacesHint')} />
        <StatCard
          value={walPending}
          label={t('dashboard.stat.pendingLabel')}
          hint={walPending === 0 ? t('dashboard.stat.pendingHintEmpty') : t('dashboard.stat.pendingHintSome')}
          tone={walPending > 0 ? 'warn' : undefined}
        />
      </div>

      {stats.instances === 0 && (
        <div className="empty-state">
          <h2>{t('dashboard.empty.title')}</h2>
          <p className="muted">{t('dashboard.empty.body')}</p>
          <button type="button" className="btn btn-primary btn-big" onClick={onConnect}>
            {t('dashboard.empty.connect')}
          </button>
        </div>
      )}

      {overview.length > 0 && (
        <div className="overview-block">
          <h2>{t('dashboard.overview.title')}</h2>
          <div className="overview-grid">
            {overview.map(a => (
              <div key={a.instance} className="overview-card">
                <div className="overview-head">
                  <strong>{AGENT_LABELS[a.type] ?? a.type}</strong>
                </div>
                <div className="overview-stats">
                  <span><b>{a.facts}</b> {t('dashboard.overview.facts')}</span>
                  <span><b>{a.themes}</b> {t('dashboard.overview.themes')}</span>
                  {a.procedures > 0 && <span><b>{a.procedures}</b> {t('dashboard.overview.procedures')}</span>}
                </div>
                {a.expertise.length > 0 && (
                  <div className="overview-expertise">
                    <span className="muted">{t('dashboard.overview.expertise')}</span>
                    {a.expertise.map(d => <span key={d} className="badge badge-theme">{d}</span>)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <details className="storage-details">
        <summary>{t('dashboard.storage.summary')}</summary>
        <p className="muted">
          {t('dashboard.storage.locationBefore')}<code>{doctor.storage_root}</code>{t('dashboard.storage.locationAfter')}
        </p>
        <table className="table">
          <thead>
            <tr>
              <th>{t('dashboard.storage.colType')}</th>
              <th>{t('dashboard.storage.colLocation')}</th>
              <th>{t('dashboard.storage.colSize')}</th>
              <th>{t('dashboard.storage.colPending')}</th>
            </tr>
          </thead>
          <tbody>
            {doctor.databases.map(db => (
              <tr key={db.path}>
                <td>{KNOWN_DB_KINDS.has(db.kind) ? t(`dashboard.dbKind.${db.kind}`) : db.kind}</td>
                <td>
                  <code className="path">{db.path}</code>
                  {!db.exists && <span className="badge badge-warn">{t('dashboard.storage.missing')}</span>}
                </td>
                <td>{db.exists ? formatBytes(db.size_bytes) : '—'}</td>
                <td>{db.wal_pending ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </>
  )
}

/**
 * Bannière moteur d'extraction : visible UNIQUEMENT quand l'extraction est
 * indisponible (avec le nombre de souvenirs en attente s'il y en a). Rien
 * d'affiché quand tout va bien.
 */
function LlmBanner({ health, onConfigure }: { health: LlmHealth | null; onConfigure?: () => void }) {
  const { t } = useT()
  if (!health || health.extraction.available) return null
  const pending = health.wal_pending
  return (
    <div className={`llm-banner${pending > 0 ? ' llm-banner-critical' : ''}`}>
      <div>
        <strong>
          ⚠️ {pending > 0
            ? t('dashboard.banner.pendingCritical', { count: pending.toLocaleString('fr-FR'), plural: pending > 1 ? 's' : '' })
            : t('dashboard.banner.noEngine')}
        </strong>
        {health.extraction.reason && <p className="muted">{health.extraction.reason}</p>}
      </div>
      {onConfigure && (
        <button type="button" className="btn btn-primary" onClick={onConfigure}>
          {t('dashboard.banner.configure')}
        </button>
      )}
    </div>
  )
}

function HealthCard({ doctor }: { doctor: DoctorReport }) {
  const { t } = useT()
  if (doctor.ok) {
    return (
      <div className="health-card health-ok">
        <span className="dot dot-ok" aria-hidden="true" />
        <div>
          <strong>{t('dashboard.health.okTitle')}</strong>
          <p className="muted">{t('dashboard.health.okBody')}</p>
        </div>
      </div>
    )
  }
  return (
    <div className="health-card health-warn">
      <span className="dot dot-warn" aria-hidden="true" />
      <div>
        <strong>{t('dashboard.health.warnTitle')}</strong>
        <ul className="warning-list">
          {doctor.warnings.map(w => (
            <li key={w}>{w}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

function StatCard({ value, label, hint, tone }: { value: number; label: string; hint: string; tone?: 'warn' }) {
  return (
    <div className={`stat-card${tone === 'warn' ? ' stat-warn' : ''}`}>
      <div className="stat-value">{value.toLocaleString('fr-FR')}</div>
      <div className="stat-label">{label}</div>
      <div className="stat-hint muted">{hint}</div>
    </div>
  )
}
