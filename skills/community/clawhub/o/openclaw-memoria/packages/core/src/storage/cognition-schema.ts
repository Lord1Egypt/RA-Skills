/**
 * Schéma des couches cognitives (bucket B « Async », spec §12) — migration
 * ADDITIVE, séparée du tronc `contentMigrations` : l'intégrateur ajoute
 * `cognitionMigrations` à la suite de la série de contenu (versions ≥ 10 pour
 * laisser la place au tronc) au moment de câbler la cognition.
 *
 * Tables :
 *  - entities    : nœuds du graphe (person/project/tool/concept/place/company) ;
 *  - relations   : arêtes NON-dirigées, 1 ligne par paire, cap poids 1.0
 *                  (modèle graph.ts legacy — la double implémentation Hebbian
 *                  incompatible est JETÉE, bug GE-5) ;
 *  - observations: synthèses agrégées par sujet (upsert obs_count, comme le
 *                  legacy self_observations/observations) ;
 *  - fact_entities : table de JOINTURE fait↔entité — REMPLACE le
 *                  `facts.entity_ids LIKE '%id%'` fragile (bug db.ts:604 / GE-3)
 *                  par un JOIN exact et indexable.
 *
 * `topics` existe déjà dans le tronc (content-schema.ts) → non recréée ici.
 *
 * Corrections gravées : PAS de colonne `status` (l'état actif = `superseded`
 * sur les faits ; les arêtes vivent par leur poids) ; `last_accessed_at` sur
 * relations pour que le decay (GE-2) soit calculable et testable.
 */
import type { Database } from 'better-sqlite3'
import { runMigrations } from './migrations.js'
import type { Migration } from './migrations.js'

export const cognitionMigrations: Migration[] = [
  {
    // Version élevée : la cognition s'ajoute APRÈS le tronc de contenu (v1).
    // L'intégrateur concatène ce tableau à `contentMigrations` ; les numéros
    // ne doivent jamais entrer en collision avec une future migration tronc.
    version: 10,
    name: 'cognition-initial',
    up(db) {
      db.exec(`
        -- ENTITÉS : nœuds du graphe. mention_count = compteur d'apparitions
        -- (sert au tri « entités les plus présentes » et au decay logique).
        CREATE TABLE entities (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          type TEXT NOT NULL DEFAULT 'concept',
          mention_count INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL
        );
        -- Unicité par nom normalisé (NOCASE) : pas deux entités « Néto »/« néto ».
        CREATE UNIQUE INDEX idx_entities_name ON entities(name COLLATE NOCASE);
        CREATE INDEX idx_entities_type ON entities(type);

        -- RELATIONS : arêtes NON-dirigées. Invariant from_entity < to_entity
        -- (ordre lexicographique) garanti à l'écriture → 1 SEULE ligne par paire
        -- quel que soit l'ordre d'extraction (anti-doublon GE-5). context = JSON
        -- array de fact_ids justifiant l'arête (cappé). weight ∈ [0, 1].
        CREATE TABLE relations (
          id TEXT PRIMARY KEY,
          from_entity TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
          to_entity TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
          kind TEXT NOT NULL DEFAULT 'related_to',
          weight REAL NOT NULL DEFAULT 0.5,
          context TEXT NOT NULL DEFAULT '[]',
          created_at TEXT NOT NULL,
          last_accessed_at TEXT NOT NULL
        );
        CREATE UNIQUE INDEX idx_relations_pair ON relations(from_entity, to_entity);
        CREATE INDEX idx_relations_from ON relations(from_entity);
        CREATE INDEX idx_relations_to ON relations(to_entity);

        -- JOINTURE fait↔entité : remplace facts.entity_ids LIKE (GE-3). Le LIKE
        -- substring était fragile (ids de longueurs variables) ; un JOIN exact
        -- est correct ET indexable dans les deux sens.
        CREATE TABLE fact_entities (
          fact_id TEXT NOT NULL,
          entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
          PRIMARY KEY (fact_id, entity_id)
        );
        CREATE INDEX idx_fact_entities_entity ON fact_entities(entity_id);

        -- OBSERVATIONS : une synthèse vivante par sujet. obs_count = nombre de
        -- faits/preuves agrégés (upsert : ré-observer un sujet incrémente, ne
        -- duplique jamais). subject porte la clé d'agrégation (sujet normalisé).
        CREATE TABLE observations (
          id TEXT PRIMARY KEY,
          subject TEXT NOT NULL,
          content TEXT NOT NULL,
          confidence REAL NOT NULL DEFAULT 0.8,
          obs_count INTEGER NOT NULL DEFAULT 1,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE UNIQUE INDEX idx_observations_subject ON observations(subject COLLATE NOCASE);
      `)
    },
  },
]

/**
 * Applique le schéma cognition à une DB de contenu (idempotent — re-run sans
 * effet). À appeler une fois par DB avant tout usage des couches cognitives.
 *
 * NOTE INTÉGRATION : ces migrations partagent la table `schema_migrations` du
 * tronc `contentMigrations` (versions ≥ 10 → pas de collision). L'intégrateur
 * peut soit appeler ce helper paresseusement, soit concaténer
 * `cognitionMigrations` à `contentMigrations` dans `ContentStore`. Tant que ce
 * n'est pas câblé dans le tronc, la cognition appelle ce helper elle-même.
 */
export function ensureCognitionSchema(db: Database): number {
  return runMigrations(db, cognitionMigrations)
}
