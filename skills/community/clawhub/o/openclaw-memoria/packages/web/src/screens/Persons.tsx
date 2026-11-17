/**
 * Personnes — qui peut parler aux agents ? Néto le plus souvent, mais aussi
 * Badette, des stagiaires, un client… Chaque personne a des identifiants
 * (numéro Telegram/WhatsApp, e-mail, handle) qui permettent à l'agent de
 * RECONNAÎTRE son interlocuteur, et des notes (rôle, ce qu'on peut partager).
 */
import { useState, type FormEvent } from 'react'
import {
  addPersonIdentifier,
  createPerson,
  deletePerson,
  getPersons,
  identifyInterlocutor,
  removePersonIdentifier,
  updatePerson,
  type InterlocutorMatch,
  type PersonIdentifier,
  type PersonProfile,
} from '../api'
import { ConfirmButton, EmptyState, ErrorBanner, Spinner, humanError, useLoad } from '../components/ui'
import { useT } from '../i18n'

type Translate = (key: string, vars?: Record<string, string | number>) => string

const KINDS: Array<{ id: PersonIdentifier['kind']; labelKey: string; placeholderKey: string }> = [
  { id: 'telegram', labelKey: 'persons.kind.telegram', placeholderKey: 'persons.placeholder.telegram' },
  { id: 'whatsapp', labelKey: 'persons.kind.whatsapp', placeholderKey: 'persons.placeholder.whatsapp' },
  { id: 'phone', labelKey: 'persons.kind.phone', placeholderKey: 'persons.placeholder.phone' },
  { id: 'email', labelKey: 'persons.kind.email', placeholderKey: 'persons.placeholder.email' },
  { id: 'handle', labelKey: 'persons.kind.handle', placeholderKey: 'persons.placeholder.handle' },
  { id: 'other', labelKey: 'persons.kind.other', placeholderKey: 'persons.placeholder.other' },
]

function kindLabel(t: Translate, kind: string): string {
  const found = KINDS.find(k => k.id === kind)
  return found ? t(found.labelKey) : kind
}

export function Persons() {
  const { t } = useT()
  const { state, reload } = useLoad(getPersons)
  const [error, setError] = useState<string | null>(null)

  return (
    <section>
      <header className="screen-head">
        <div>
          <h1>{t('persons.title')}</h1>
          <p className="muted">
            {t('persons.lead.before')}<strong>{t('persons.lead.strong')}</strong>{t('persons.lead.after')}
          </p>
        </div>
      </header>

      {error && <ErrorBanner message={error} />}

      <IdentifyTester onError={setError} />

      <AddPerson onAdded={reload} onError={setError} />

      {state.status === 'loading' && <Spinner />}
      {state.status === 'error' && <ErrorBanner message={state.message} onRetry={reload} />}
      {state.status === 'ready' &&
        (state.data.length === 0 ? (
          <EmptyState title={t('persons.empty.title')} body={t('persons.empty.body')} />
        ) : (
          <ul className="person-list">
            {state.data.map(p => (
              <PersonCard key={p.id} person={p} onChange={reload} onError={setError} />
            ))}
          </ul>
        ))}
    </section>
  )
}

function IdentifyTester({ onError }: { onError: (m: string) => void }) {
  const { t } = useT()
  const [kind, setKind] = useState<PersonIdentifier['kind'] | 'name'>('telegram')
  const [value, setValue] = useState('')
  const [result, setResult] = useState<InterlocutorMatch | null | 'none'>(null)

  const test = async (e: FormEvent) => {
    e.preventDefault()
    if (!value.trim()) return
    try {
      const input = kind === 'name' ? { name: value } : { [kind]: value }
      const match = await identifyInterlocutor(input)
      setResult(match ?? 'none')
    } catch (err) {
      onError(humanError(err))
    }
  }

  return (
    <div className="settings-block">
      <h2>{t('persons.identify.title')}</h2>
      <p className="muted">{t('persons.identify.lead')}</p>
      <form className="identify-row" onSubmit={test}>
        <select value={kind} onChange={e => setKind(e.target.value as PersonIdentifier['kind'] | 'name')}>
          {KINDS.map(k => <option key={k.id} value={k.id}>{t(k.labelKey)}</option>)}
          <option value="name">{t('persons.identify.name')}</option>
        </select>
        <input type="text" value={value} placeholder={t('persons.identify.placeholder')} onChange={e => setValue(e.target.value)} />
        <button type="submit" className="btn btn-primary">{t('persons.identify.submit')}</button>
      </form>
      {result === 'none' && <p className="muted" style={{ marginTop: '0.6rem' }}>{t('persons.identify.noMatch')}</p>}
      {result && result !== 'none' && (
        <div className="identify-result">
          <strong>{result.person.display_name}</strong>
          {result.person.relation && <span className="badge badge-theme">{result.person.relation}</span>}
          {result.person.notes && <p className="muted">{result.person.notes}</p>}
          {result.known.length > 0 && (
            <ul className="fact-list">
              {result.known.slice(0, 5).map((f, i) => <li key={i} className="fact-card"><p className="fact-content">{f}</p></li>)}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}

function AddPerson({ onAdded, onError }: { onAdded: () => void; onError: (m: string) => void }) {
  const { t } = useT()
  const [name, setName] = useState('')
  const [relation, setRelation] = useState('')
  const [busy, setBusy] = useState(false)

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    setBusy(true)
    try {
      await createPerson({ display_name: name.trim(), relation: relation.trim() || undefined })
      setName('')
      setRelation('')
      onAdded()
    } catch (err) {
      onError(humanError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="add-person" onSubmit={submit}>
      <input type="text" value={name} placeholder={t('persons.add.namePlaceholder')} onChange={e => setName(e.target.value)} />
      <input type="text" value={relation} placeholder={t('persons.add.relationPlaceholder')} onChange={e => setRelation(e.target.value)} />
      <button type="submit" className="btn btn-primary" disabled={busy || !name.trim()}>{t('persons.add.submit')}</button>
    </form>
  )
}

function PersonCard({ person, onChange, onError }: { person: PersonProfile; onChange: () => void; onError: (m: string) => void }) {
  const { t } = useT()
  const [notes, setNotes] = useState(person.notes ?? '')
  const [relation, setRelation] = useState(person.relation ?? '')
  const [idKind, setIdKind] = useState<PersonIdentifier['kind']>('telegram')
  const [idValue, setIdValue] = useState('')

  const saveMeta = async () => {
    try {
      await updatePerson(person.id, { relation: relation.trim() || null, notes: notes.trim() || null })
      onChange()
    } catch (err) {
      onError(humanError(err))
    }
  }

  const addId = async (e: FormEvent) => {
    e.preventDefault()
    if (!idValue.trim()) return
    try {
      await addPersonIdentifier(person.id, idKind, idValue.trim())
      setIdValue('')
      onChange()
    } catch (err) {
      onError(humanError(err))
    }
  }

  const dirty = notes !== (person.notes ?? '') || relation !== (person.relation ?? '')

  return (
    <li className="person-card">
      <div className="person-head">
        <strong>{person.display_name}</strong>
        {person.user_id && <span className="badge badge-ok">{t('persons.card.userBadge')}</span>}
        <ConfirmButton label={t('persons.card.delete')} confirmLabel={t('persons.card.deleteConfirm')} onConfirm={async () => {
          try { await deletePerson(person.id); onChange() } catch (err) { onError(humanError(err)) }
        }} />
      </div>

      <div className="person-fields">
        <input type="text" value={relation} placeholder={t('persons.card.relationPlaceholder')} onChange={e => setRelation(e.target.value)} />
        <textarea value={notes} placeholder={t('persons.card.notesPlaceholder')} onChange={e => setNotes(e.target.value)} rows={2} />
        {dirty && <button type="button" className="btn btn-primary" onClick={() => void saveMeta()}>{t('persons.card.save')}</button>}
      </div>

      <div className="person-idents">
        {person.identifiers.length === 0 && <span className="muted">{t('persons.card.noIdent')}</span>}
        {person.identifiers.map(id => (
          <span key={id.id} className="ident-chip">
            <span className="ident-kind">{kindLabel(t, id.kind)}</span> {id.value}
            <button type="button" className="ident-x" aria-label={t('persons.card.removeIdent')} onClick={async () => {
              try { await removePersonIdentifier(id.id); onChange() } catch (err) { onError(humanError(err)) }
            }}>✕</button>
          </span>
        ))}
      </div>

      <form className="ident-add" onSubmit={addId}>
        <select value={idKind} onChange={e => setIdKind(e.target.value as PersonIdentifier['kind'])}>
          {KINDS.map(k => <option key={k.id} value={k.id}>{t(k.labelKey)}</option>)}
        </select>
        <input type="text" value={idValue} placeholder={t(KINDS.find(k => k.id === idKind)!.placeholderKey)} onChange={e => setIdValue(e.target.value)} />
        <button type="submit" className="btn btn-ghost" disabled={!idValue.trim()}>{t('persons.card.addIdent')}</button>
      </form>
    </li>
  )
}
