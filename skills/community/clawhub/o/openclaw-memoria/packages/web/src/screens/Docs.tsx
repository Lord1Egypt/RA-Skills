/**
 * Docs — centre de documentation intégré. Aucune donnée, aucun appel réseau :
 * du contenu statique, organisé en SECTIONS (sous-onglets) regroupées par
 * thème, pour que quelqu'un qui ouvre Memoria comprenne le produit de fond en
 * comble — concepts, onglets, moteur d'IA, partage, multi-machines, CLI, FAQ.
 *
 * Tenir à jour quand on ajoute un écran, une commande CLI ou un provider.
 * Le contenu reflète le code réel (cli/commands, core/llm, core/sync,
 * core/cognition, docs/v3). Pas de promesse non tenue.
 */
import { useState, type ReactNode } from 'react'
import { useT } from '../i18n'

type Translate = (key: string, vars?: Record<string, string | number>) => string

// --------------------------------------------------------------- présentation

function Lead({ children }: { children: ReactNode }) {
  return <p className="docs-lead">{children}</p>
}

function Callout({ kind = 'info', children }: { kind?: 'info' | 'tip' | 'warn'; children: ReactNode }) {
  return <div className={`docs-callout${kind === 'info' ? '' : ` ${kind}`}`}>{children}</div>
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="settings-block">
      <h2>{title}</h2>
      {children}
    </div>
  )
}

// ------------------------------------------------------------------- sections

function Bienvenue() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.welcome.title')}</h1>
      <Lead>{t('docs.welcome.lead')}</Lead>

      <div className="vault-explainer">
        <strong>{t('docs.welcome.oneline.label')}</strong> {t('docs.welcome.oneline.body')}
      </div>

      <Section title={t('docs.welcome.principles.title')}>
        <ul>
          <li>
            <strong>{t('docs.welcome.principle.local.title')}</strong> {t('docs.welcome.principle.local.body')}
          </li>
          <li>
            <strong>{t('docs.welcome.principle.peragent.title')}</strong> {t('docs.welcome.principle.peragent.body')}
          </li>
          <li>
            <strong>{t('docs.welcome.principle.govern.title')}</strong> {t('docs.welcome.principle.govern.body')}
          </li>
          <li>
            <strong>{t('docs.welcome.principle.secrets.title')}</strong> {t('docs.welcome.principle.secrets.body')}
          </li>
          <li>
            <strong>{t('docs.welcome.principle.isolation.title')}</strong> {t('docs.welcome.principle.isolation.body')}
          </li>
        </ul>
      </Section>

      <Callout kind="tip">
        {t('docs.welcome.cta.p1')}{' '}<strong>{t('docs.welcome.cta.quickstart')}</strong>{' '}{t('docs.welcome.cta.p2')}{' '}
        <strong>{t('docs.welcome.cta.how')}</strong>{' '}{t('docs.welcome.cta.p3')}
      </Callout>
    </div>
  )
}

function Demarrage() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.start.title')}</h1>
      <Lead>{t('docs.start.lead')}</Lead>

      <Section title={t('docs.start.install.title')}>
        <p>{t('docs.start.install.p')}</p>
        <pre className="command">curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/memoria-v1/scripts/install-memoria.sh | sh</pre>
        <p className="muted">
          {t('docs.start.install.note1')}{' '}<code>memoria ui</code>.
        </p>
      </Section>

      <Section title={t('docs.start.engine.title')}>
        <p>{t('docs.start.engine.p')}</p>
        <ul>
          <li><strong>Ollama</strong> {t('docs.start.engine.ollama')}</li>
          <li><strong>LM Studio</strong> {t('docs.start.engine.lmstudio')}</li>
          <li><strong>{t('docs.start.engine.apikey.label')}</strong> {t('docs.start.engine.apikey.desc')}</li>
        </ul>
        <p className="muted">
          {t('docs.start.engine.more.p1')}{' '}<strong>{t('docs.start.engine.more.link')}</strong>{t('docs.start.engine.more.p2')}{' '}
          <strong>{t('docs.start.engine.more.settings')}</strong>.
        </p>
      </Section>

      <Section title={t('docs.start.connect.title')}>
        <p>
          {t('docs.start.connect.p1')}{' '}<strong>{t('docs.start.connect.agents')}</strong>{' '}{t('docs.start.connect.p2')}{' '}
          <strong>{t('docs.start.connect.button')}</strong>{' '}{t('docs.start.connect.p3')}
        </p>
        <p className="muted">
          {t('docs.start.connect.remote.p1')}{' '}<strong>{t('docs.start.connect.remote.pairing')}</strong>{' '}
          {t('docs.start.connect.remote.p2')}{' '}<code>memoria pair claude-code</code>.
        </p>
      </Section>

      <Section title={t('docs.start.import.title')}>
        <p>
          {t('docs.start.import.p1')}{' '}<strong>{t('docs.start.import.agents')}</strong>{t('docs.start.import.p2')}{' '}
          <strong>{t('docs.start.import.button')}</strong>{' '}{t('docs.start.import.p3')}{' '}
          <strong>{t('docs.start.import.review')}</strong>{' '}{t('docs.start.import.p4')}
        </p>
      </Section>

      <Callout kind="tip">
        {t('docs.start.cta.p1')}{' '}<strong>{t('docs.start.cta.autocapture')}</strong>{t('docs.start.cta.p2')}{' '}
        <strong>{t('docs.start.cta.themes')}</strong>{' '}{t('docs.start.cta.p3')}
      </Callout>
    </div>
  )
}

function CommentCaMarche() {
  const { t } = useT()
  const pieces = [
    { title: t('docs.how.piece.daemon.title'), body: t('docs.how.piece.daemon.body') },
    { title: t('docs.how.piece.mcp.title'), body: t('docs.how.piece.mcp.body') },
    { title: t('docs.how.piece.core.title'), body: t('docs.how.piece.core.body') },
    { title: t('docs.how.piece.ui.title'), body: t('docs.how.piece.ui.body') },
  ]
  return (
    <div className="docs-body">
      <h1>{t('docs.how.title')}</h1>
      <Lead>{t('docs.how.lead')}</Lead>

      <Section title={t('docs.how.pieces.title')}>
        <div className="layer-grid">
          {pieces.map(x => (
            <div key={x.title} className="layer-card">
              <strong>{x.title}</strong>
              <p className="layer-desc muted">{x.body}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section title={t('docs.how.cycle.title')}>
        <ol className="docs-steps">
          <li><strong>{t('docs.how.cycle.capture.title')}</strong> {t('docs.how.cycle.capture.body')}</li>
          <li><strong>{t('docs.how.cycle.extraction.title')}</strong> {t('docs.how.cycle.extraction.body')}</li>
          <li><strong>{t('docs.how.cycle.sort.title')}</strong> {t('docs.how.cycle.sort.body')}</li>
          <li><strong>{t('docs.how.cycle.recall.title')}</strong> {t('docs.how.cycle.recall.body')}</li>
        </ol>
      </Section>

      <Callout>
        {t('docs.how.callout.p1')}{' '}<strong>{t('docs.how.callout.mode')}</strong>{t('docs.how.callout.p2')}
      </Callout>
    </div>
  )
}

function Souvenirs() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.memories.title')}</h1>
      <Lead>{t('docs.memories.lead')}</Lead>

      <Section title={t('docs.memories.what.title')}>
        <p>
          {t('docs.memories.what.p1')}{' '}<strong>{t('docs.memories.what.provenance')}</strong>{' '}{t('docs.memories.what.p2')}{' '}
          <strong>{t('docs.memories.what.really')}</strong>{' '}{t('docs.memories.what.p3')}
        </p>
      </Section>

      <Section title={t('docs.memories.spaces.title')}>
        <p>
          {t('docs.memories.spaces.p1')}{' '}<strong>{t('docs.memories.spaces.private')}</strong>{' '}{t('docs.memories.spaces.p2')}{' '}
          <strong>{t('docs.memories.spaces.shared')}</strong>{' '}{t('docs.memories.spaces.p3')}
        </p>
        <ul>
          <li><strong>user</strong> {t('docs.memories.scope.user')}</li>
          <li><strong>org</strong> {t('docs.memories.scope.org')}</li>
          <li><strong>client</strong> / <strong>project</strong> {t('docs.memories.scope.clientproject')}</li>
          <li><strong>{t('docs.memories.scope.subject.label')}</strong> {t('docs.memories.scope.subject.desc')}</li>
        </ul>
        <p className="muted">
          {t('docs.memories.spaces.note.p1')}{' '}<strong>{t('docs.memories.spaces.note.sharing')}</strong>).
        </p>
      </Section>

      <Callout kind="tip">
        {t('docs.memories.cta.p1')}{' '}<strong>{t('docs.memories.cta.themes')}</strong>{' '}{t('docs.memories.cta.p2')}
      </Callout>
    </div>
  )
}

function Capture() {
  const { t } = useT()
  const modes = [
    { label: t('docs.capture.mode.auto.label'), body: t('docs.capture.mode.auto.body') },
    { label: t('docs.capture.mode.review.label'), body: t('docs.capture.mode.review.body') },
    { label: t('docs.capture.mode.pause.label'), body: t('docs.capture.mode.pause.body') },
  ]
  return (
    <div className="docs-body">
      <h1>{t('docs.capture.title')}</h1>
      <Lead>{t('docs.capture.lead')}</Lead>
      <div className="layer-grid">
        {modes.map(m => (
          <div key={m.label} className="layer-card">
            <strong>{m.label}</strong>
            <p className="layer-desc muted">{m.body}</p>
          </div>
        ))}
      </div>
      <Callout>
        {t('docs.capture.callout.p1')}{' '}<code>memoria disable</code>{' '}{t('docs.capture.callout.p2')}{' '}
        <code>memoria enable</code>{' '}{t('docs.capture.callout.p3')}
      </Callout>
    </div>
  )
}

function Moteur() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.engine.title')}</h1>
      <Lead>
        {t('docs.engine.lead.p1')}{' '}<strong>{t('docs.engine.lead.settings')}</strong>.
      </Lead>

      <Section title={t('docs.engine.providers.title')}>
        <table className="docs-table">
          <thead>
            <tr>
              <th>{t('docs.engine.table.provider')}</th>
              <th>{t('docs.engine.table.type')}</th>
              <th>{t('docs.engine.table.model')}</th>
              <th>{t('docs.engine.table.note')}</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><strong>Ollama</strong></td><td>{t('docs.engine.type.local')}</td><td><code>qwen2.5:3b</code></td><td>{t('docs.engine.row.ollama.note')}</td></tr>
            <tr><td>LM Studio</td><td>{t('docs.engine.type.local')}</td><td>{t('docs.engine.row.lmstudio.model')}</td><td>{t('docs.engine.row.lmstudio.note')}</td></tr>
            <tr><td>OpenAI</td><td>{t('docs.engine.type.cloud')}</td><td><code>gpt-4o-mini</code></td><td>{t('docs.engine.row.openai.note')}</td></tr>
            <tr><td>Anthropic</td><td>{t('docs.engine.type.cloud')}</td><td><code>claude-haiku-4-5</code></td><td>{t('docs.engine.row.anthropic.note')}</td></tr>
            <tr><td>OpenRouter</td><td>{t('docs.engine.type.cloud')}</td><td>{t('docs.engine.row.openrouter.model')}</td><td>{t('docs.engine.row.openrouter.note')}</td></tr>
          </tbody>
        </table>
        <p className="muted">{t('docs.engine.providers.note')}</p>
      </Section>

      <Section title={t('docs.engine.embeddings.title')}>
        <p>
          {t('docs.engine.embeddings.p1')}{' '}<em>{t('docs.engine.embeddings.sens')}</em>{' '}{t('docs.engine.embeddings.p2')}{' '}
          <strong>{t('docs.engine.embeddings.ollamaonly')}</strong>{t('docs.engine.embeddings.p3')}{' '}<code>nomic-embed-text</code>{' '}
          {t('docs.engine.embeddings.p4')}
        </p>
      </Section>

      <Section title={t('docs.engine.degraded.title')}>
        <p>
          {t('docs.engine.degraded.p1')}{' '}<strong>{t('docs.engine.degraded.strong')}</strong>{t('docs.engine.degraded.p2')}
        </p>
      </Section>

      <Callout kind="tip">
        {t('docs.engine.callout.p1')}{' '}<code>ollama pull qwen2.5:3b</code>{' '}{t('docs.engine.callout.p2')}{' '}
        <code>ollama pull nomic-embed-text</code>{t('docs.engine.callout.p3')}
      </Callout>
    </div>
  )
}

function Couches() {
  const { t } = useT()
  const buckets = [
    { name: t('docs.layers.bucket.a.name'), desc: t('docs.layers.bucket.a.desc') },
    { name: t('docs.layers.bucket.b.name'), desc: t('docs.layers.bucket.b.desc') },
    { name: t('docs.layers.bucket.c.name'), desc: t('docs.layers.bucket.c.desc') },
    { name: t('docs.layers.bucket.d.name'), desc: t('docs.layers.bucket.d.desc') },
  ]
  return (
    <div className="docs-body">
      <h1>{t('docs.layers.title')}</h1>
      <Lead>
        {t('docs.layers.lead.p1')}{' '}<strong>{t('docs.layers.lead.layers')}</strong>{' '}{t('docs.layers.lead.p2')}{' '}
        <strong>{t('docs.layers.lead.system')}</strong>.
      </Lead>
      <div className="layer-grid">
        {buckets.map(b => (
          <div key={b.name} className="layer-card">
            <strong>{b.name}</strong>
            <p className="layer-desc muted">{b.desc}</p>
          </div>
        ))}
      </div>

      <Section title={t('docs.layers.recall.title')}>
        <p>{t('docs.layers.recall.p')}</p>
        <ul>
          <li><strong>{t('docs.layers.recall.fulltext.label')}</strong> {t('docs.layers.recall.fulltext.desc')}</li>
          <li><strong>{t('docs.layers.recall.semantic.label')}</strong> {t('docs.layers.recall.semantic.desc')}</li>
          <li><strong>{t('docs.layers.recall.graph.label')}</strong> {t('docs.layers.recall.graph.desc')}</li>
          <li><strong>Hot-tier</strong> {t('docs.layers.recall.hottier.desc')}</li>
        </ul>
        <p className="muted">{t('docs.layers.recall.note')}</p>
      </Section>
    </div>
  )
}

function tabGroups(t: Translate): Array<{ title: string; tabs: Array<{ label: string; goal: string; details: string[] }> }> {
  return [
    {
      title: t('docs.tabs.group.pilotage'),
      tabs: [
        {
          label: t('docs.tabs.dashboard.label'),
          goal: t('docs.tabs.dashboard.goal'),
          details: [t('docs.tabs.dashboard.detail.1'), t('docs.tabs.dashboard.detail.2'), t('docs.tabs.dashboard.detail.3')],
        },
        {
          label: t('docs.tabs.agents.label'),
          goal: t('docs.tabs.agents.goal'),
          details: [t('docs.tabs.agents.detail.1'), t('docs.tabs.agents.detail.2'), t('docs.tabs.agents.detail.3')],
        },
      ],
    },
    {
      title: t('docs.tabs.group.memory'),
      tabs: [
        {
          label: t('docs.tabs.memory.label'),
          goal: t('docs.tabs.memory.goal'),
          details: [t('docs.tabs.memory.detail.1'), t('docs.tabs.memory.detail.2')],
        },
        {
          label: t('docs.tabs.themes.label'),
          goal: t('docs.tabs.themes.goal'),
          details: [t('docs.tabs.themes.detail.1'), t('docs.tabs.themes.detail.2')],
        },
        {
          label: t('docs.tabs.recurrences.label'),
          goal: t('docs.tabs.recurrences.goal'),
          details: [t('docs.tabs.recurrences.detail.1'), t('docs.tabs.recurrences.detail.2')],
        },
        {
          label: t('docs.tabs.procedures.label'),
          goal: t('docs.tabs.procedures.goal'),
          details: [t('docs.tabs.procedures.detail.1'), t('docs.tabs.procedures.detail.2')],
        },
      ],
    },
    {
      title: t('docs.tabs.group.control'),
      tabs: [
        {
          label: t('docs.tabs.review.label'),
          goal: t('docs.tabs.review.goal'),
          details: [t('docs.tabs.review.detail.1'), t('docs.tabs.review.detail.2')],
        },
        {
          label: t('docs.tabs.revisions.label'),
          goal: t('docs.tabs.revisions.goal'),
          details: [t('docs.tabs.revisions.detail.1'), t('docs.tabs.revisions.detail.2')],
        },
      ],
    },
    {
      title: t('docs.tabs.group.sharing'),
      tabs: [
        {
          label: t('docs.tabs.sharing.label'),
          goal: t('docs.tabs.sharing.goal'),
          details: [t('docs.tabs.sharing.detail.1'), t('docs.tabs.sharing.detail.2'), t('docs.tabs.sharing.detail.3')],
        },
        {
          label: t('docs.tabs.people.label'),
          goal: t('docs.tabs.people.goal'),
          details: [t('docs.tabs.people.detail.1'), t('docs.tabs.people.detail.2')],
        },
      ],
    },
    {
      title: t('docs.tabs.group.security'),
      tabs: [
        {
          label: t('docs.tabs.vault.label'),
          goal: t('docs.tabs.vault.goal'),
          details: [t('docs.tabs.vault.detail.1'), t('docs.tabs.vault.detail.2'), t('docs.tabs.vault.detail.3')],
        },
        {
          label: t('docs.tabs.system.label'),
          goal: t('docs.tabs.system.goal'),
          details: [t('docs.tabs.system.detail.1'), t('docs.tabs.system.detail.2')],
        },
        {
          label: t('docs.tabs.journal.label'),
          goal: t('docs.tabs.journal.goal'),
          details: [t('docs.tabs.journal.detail.1'), t('docs.tabs.journal.detail.2')],
        },
        {
          label: t('docs.tabs.settings.label'),
          goal: t('docs.tabs.settings.goal'),
          details: [t('docs.tabs.settings.detail.1'), t('docs.tabs.settings.detail.2')],
        },
      ],
    },
  ]
}

function GuideOnglets() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.tabs.title')}</h1>
      <Lead>{t('docs.tabs.lead')}</Lead>
      {tabGroups(t).map(group => (
        <Section key={group.title} title={group.title}>
          <div className="layer-grid">
            {group.tabs.map(tab => (
              <div key={tab.label} className="layer-card">
                <strong>{tab.label}</strong>
                <p className="layer-desc">{tab.goal}</p>
                <ul className="docs-points muted">
                  {tab.details.map((d, i) => <li key={i}>{d}</li>)}
                </ul>
              </div>
            ))}
          </div>
        </Section>
      ))}
    </div>
  )
}

function Partage() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.sharing.title')}</h1>
      <Lead>{t('docs.sharing.lead')}</Lead>

      <Section title={t('docs.sharing.tools.title')}>
        <ul>
          <li>
            <strong>{t('docs.sharing.tools.matrix.label')}</strong> {t('docs.sharing.tools.matrix.desc')}
          </li>
          <li>
            <strong>{t('docs.sharing.tools.facts.label')}</strong> {t('docs.sharing.tools.facts.desc')}
          </li>
        </ul>
      </Section>

      <Section title={t('docs.sharing.people.title')}>
        <p>
          {t('docs.sharing.people.p1')}{' '}<strong>{t('docs.sharing.people.tab')}</strong>{' '}{t('docs.sharing.people.p2')}{' '}
          <em>{t('docs.sharing.people.q')}</em>{' '}{t('docs.sharing.people.p3')}{' '}<strong>{t('docs.sharing.people.recognizes')}</strong>{' '}
          {t('docs.sharing.people.p4')}
        </p>
      </Section>

      <Callout kind="warn">
        {t('docs.sharing.callout.p1')}{' '}<strong>{t('docs.sharing.callout.strong')}</strong>{' '}{t('docs.sharing.callout.p2')}
      </Callout>
    </div>
  )
}

function MultiMachines() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.sync.title')}</h1>
      <Lead>{t('docs.sync.lead')}</Lead>

      <Section title={t('docs.sync.model.title')}>
        <p>
          {t('docs.sync.model.p1')}{' '}<strong>{t('docs.sync.model.hub')}</strong>{' '}{t('docs.sync.model.p2')}
          <strong>{t('docs.sync.model.spokes')}</strong>{t('docs.sync.model.p3')}{' '}<strong>{t('docs.sync.model.offline')}</strong>{' '}
          {t('docs.sync.model.p4')}
        </p>
      </Section>

      <Section title={t('docs.sync.setup.title')}>
        <ol className="docs-steps">
          <li>{t('docs.sync.setup.step1.p1')}{' '}<code>memoria sync init-hub</code>{t('docs.sync.setup.step1.p2')}</li>
          <li>{t('docs.sync.setup.step2.p1')}{' '}<code>memoria sync invite</code>{' '}{t('docs.sync.setup.step2.p2')}</li>
          <li>{t('docs.sync.setup.step3.p1')}{' '}<code>{'memoria sync join --hub <ip:port> --code XXXX-XXXX'}</code>.</li>
        </ol>
        <p className="muted">{t('docs.sync.setup.note')}</p>
      </Section>

      <Section title={t('docs.sync.flow.title')}>
        <ul>
          <li><strong>{t('docs.sync.flow.synced.label')}</strong> {t('docs.sync.flow.synced.desc')}</li>
          <li><strong>{t('docs.sync.flow.never.label')}</strong> {t('docs.sync.flow.never.desc')}</li>
        </ul>
      </Section>

      <Callout>{t('docs.sync.callout')}</Callout>
    </div>
  )
}

function Securite() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.security.title')}</h1>
      <Lead>{t('docs.security.lead')}</Lead>

      <Section title={t('docs.security.local.title')}>
        <p>{t('docs.security.local.body')}</p>
      </Section>

      <Section title={t('docs.security.secrets.title')}>
        <p>
          {t('docs.security.secrets.p1')}{' '}<strong>{t('docs.security.secrets.vault')}</strong>{' '}{t('docs.security.secrets.p2')}{' '}
          <strong>{t('docs.security.secrets.reference')}</strong>{t('docs.security.secrets.p3')}
        </p>
      </Section>

      <Section title={t('docs.security.isolation.title')}>
        <p>
          {t('docs.security.isolation.p1')}{' '}<strong>{t('docs.security.isolation.strong')}</strong>.
        </p>
      </Section>

      <Section title={t('docs.security.trace.title')}>
        <p>
          {t('docs.security.trace.p1')}{' '}<strong>{t('docs.security.trace.journal')}</strong>{' '}{t('docs.security.trace.p2')}{' '}
          <em>{t('docs.security.trace.never')}</em>{' '}{t('docs.security.trace.p3')}{' '}<code>forget</code>{' '}{t('docs.security.trace.p4')}
        </p>
      </Section>
    </div>
  )
}

function cliGroups(t: Translate): Array<{ title: string; cmds: Array<[string, string]> }> {
  return [
    {
      title: t('docs.cli.group.start'),
      cmds: [
        ['memoria', t('docs.cli.memoria')],
        ['memoria init', t('docs.cli.init')],
        ['memoria start / stop', t('docs.cli.startstop')],
        ['memoria autostart on|off', t('docs.cli.autostart')],
        ['memoria update', t('docs.cli.update')],
      ],
    },
    {
      title: t('docs.cli.group.agents'),
      cmds: [
        ['memoria pair <type>', t('docs.cli.pair')],
        ['memoria agents', t('docs.cli.agents')],
        ['memoria revoke <id>', t('docs.cli.revoke')],
        ['memoria delete-agent <id>', t('docs.cli.deleteagent')],
      ],
    },
    {
      title: t('docs.cli.group.memory'),
      cmds: [
        ['memoria import --instance <id>', t('docs.cli.import')],
        ['memoria export', t('docs.cli.export')],
        ['memoria forget --id … / --query …', t('docs.cli.forget')],
        ['memoria stats', t('docs.cli.stats')],
        ['memoria doctor', t('docs.cli.doctor')],
        ['memoria audit', t('docs.cli.audit')],
      ],
    },
    {
      title: t('docs.cli.group.control'),
      cmds: [
        ['memoria disable / enable', t('docs.cli.disableenable')],
        ['memoria move --to <chemin>', t('docs.cli.move')],
      ],
    },
    {
      title: t('docs.cli.group.sync'),
      cmds: [
        ['memoria sync status', t('docs.cli.syncstatus')],
        ['memoria sync init-hub', t('docs.cli.syncinithub')],
        ['memoria sync invite', t('docs.cli.syncinvite')],
        ['memoria sync join --hub … --code …', t('docs.cli.syncjoin')],
        ['memoria sync now', t('docs.cli.syncnow')],
        ['memoria sync leave', t('docs.cli.syncleave')],
      ],
    },
  ]
}

function Cli() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.cli.title')}</h1>
      <Lead>
        {t('docs.cli.lead.p1')}{' '}<code>memoria</code>. {t('docs.cli.lead.p2')}{' '}<code>--help</code>{' '}{t('docs.cli.lead.p3')}
      </Lead>
      {cliGroups(t).map(group => (
        <Section key={group.title} title={group.title}>
          <table className="docs-table">
            <tbody>
              {group.cmds.map(([cmd, desc]) => (
                <tr key={cmd}>
                  <td><code>{cmd}</code></td>
                  <td>{desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>
      ))}
    </div>
  )
}

function faqItems(t: Translate): Array<{ q: string; a: ReactNode }> {
  return [
    {
      q: t('docs.faq.engine.q'),
      a: <>{t('docs.faq.engine.a1')}{' '}<strong>{t('docs.faq.engine.settings')}</strong>{t('docs.faq.engine.a2')}</>,
    },
    {
      q: t('docs.faq.down.q'),
      a: <>{t('docs.faq.down.a1')}{' '}<code>memoria start</code>{' '}{t('docs.faq.down.a2')}{' '}<code>memoria</code>{' '}{t('docs.faq.down.a3')}</>,
    },
    {
      q: t('docs.faq.cache.q'),
      a: <>{t('docs.faq.cache.a1')}<code>{'memoria stop && memoria start'}</code>{t('docs.faq.cache.a2')}</>,
    },
    {
      q: t('docs.faq.nomemory.q'),
      a: (
        <>
          {t('docs.faq.nomemory.a1')}{' '}<strong>{t('docs.faq.nomemory.capture')}</strong>{' '}{t('docs.faq.nomemory.a2')}{' '}
          <strong>{t('docs.faq.nomemory.pause')}</strong>{t('docs.faq.nomemory.a3')}{' '}<strong>{t('docs.faq.nomemory.agents')}</strong>
          {t('docs.faq.nomemory.a4')}
        </>
      ),
    },
    {
      q: t('docs.faq.delete.q'),
      a: (
        <>
          {t('docs.faq.delete.a1')}{' '}<strong>{t('docs.faq.delete.memory')}</strong>{' '}{t('docs.faq.delete.a2')}{' '}
          <code>{'memoria forget --query "…"'}</code>.
        </>
      ),
    },
    {
      q: t('docs.faq.data.q'),
      a: <>{t('docs.faq.data.a1')}{' '}<em>{t('docs.faq.data.cloud')}</em>{' '}{t('docs.faq.data.a2')}</>,
    },
    {
      q: t('docs.faq.update.q'),
      a: <><code>memoria update</code>{' '}{t('docs.faq.update.a1')}{' '}<strong>{t('docs.faq.update.settings')}</strong>.</>,
    },
  ]
}

function Faq() {
  const { t } = useT()
  return (
    <div className="docs-body">
      <h1>{t('docs.faq.title')}</h1>
      <Lead>{t('docs.faq.lead')}</Lead>
      {faqItems(t).map((item, i) => (
        <Section key={i} title={item.q}>
          <p>{item.a}</p>
        </Section>
      ))}
      <Callout kind="tip">
        {t('docs.faq.callout.p1')}{' '}<code>memoria doctor</code>{' '}{t('docs.faq.callout.p2')}
      </Callout>
    </div>
  )
}

// --------------------------------------------------------------------- navigation

type DocSection = { id: string; group: string; render: () => ReactNode }

const SECTIONS: DocSection[] = [
  { id: 'welcome', group: 'start', render: () => <Bienvenue /> },
  { id: 'start', group: 'start', render: () => <Demarrage /> },
  { id: 'how', group: 'start', render: () => <CommentCaMarche /> },
  { id: 'memories', group: 'concepts', render: () => <Souvenirs /> },
  { id: 'capture', group: 'concepts', render: () => <Capture /> },
  { id: 'engine', group: 'concepts', render: () => <Moteur /> },
  { id: 'layers', group: 'concepts', render: () => <Couches /> },
  { id: 'tabs', group: 'use', render: () => <GuideOnglets /> },
  { id: 'sharing', group: 'use', render: () => <Partage /> },
  { id: 'sync', group: 'use', render: () => <MultiMachines /> },
  { id: 'security', group: 'reference', render: () => <Securite /> },
  { id: 'cli', group: 'reference', render: () => <Cli /> },
  { id: 'faq', group: 'reference', render: () => <Faq /> },
]

const GROUP_ORDER = ['start', 'concepts', 'use', 'reference']

export function Docs() {
  const { t } = useT()
  const [active, setActive] = useState<string>(SECTIONS[0]?.id ?? 'welcome')
  const current = SECTIONS.find(s => s.id === active) ?? SECTIONS[0]

  if (!current) return null

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('docs.header.title')}</h1>
          <p className="muted">{t('docs.header.lead')}</p>
        </div>
      </header>

      <div className="docs-layout">
        <nav className="docs-subnav" aria-label={t('docs.nav.aria')}>
          {GROUP_ORDER.map(group => (
            <div key={group}>
              <div className="docs-subnav-group">{t(`docs.group.${group}`)}</div>
              {SECTIONS.filter(s => s.group === group).map(s => (
                <button
                  key={s.id}
                  type="button"
                  className={`${active === s.id ? 'docs-active' : ''}`}
                  onClick={() => setActive(s.id)}
                >
                  {t(`docs.nav.${s.id}`)}
                </button>
              ))}
            </div>
          ))}
        </nav>
        <div>{current.render()}</div>
      </div>
    </section>
  )
}
