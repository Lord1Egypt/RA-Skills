// Muninn v5.2 - Sleep Cycle Consolidation
// Runs at 2:00 AM to compress Hippocampal observations into Cortex Prototypes
// + Auto-forgetting (Supermemory parity)

import OpenAI from 'openai';
import dotenv from 'dotenv';
import { Pool } from 'pg';
import cron from 'node-cron';
import { runForgettingCycle, ForgettingResult } from './forgetting/index.js';

dotenv.config();

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// ============================================
// FORGETTING CYCLE (SQLite version)
// ============================================

async function runForgettingCycleSQLite(): Promise<ForgettingResult> {
  // For SQLite-based databases
  const Database = require('better-sqlite3');
  const dbPath = process.env.MUNINN_DB_PATH || '/tmp/muninn-v2.db';
  const db = new Database(dbPath);
  
  try {
    const result = await runForgettingCycle(db);
    return result;
  } finally {
    db.close();
  }
}

// ============================================
// CONSOLIDATION PROMPT (from sleep-cycle-prompt.md)
// ============================================

const SLEEP_CYCLE_PROMPT = `You are the Cortex Consolidation Engine for Muninn v5.2.

You are reviewing 24 hours of newly ingested "Hippocampal" observations.
Current Date: {{current_date}}

## Input Data

### Raw Observations (Hippocampal Layer)
{{observations}}

### Decision Trace Rewards (Today's Successful Retrievals)
{{decision_traces}}

## Your Task

1. **Identify Atomic Clusters**: Group observations into themes (CAREER, WELLNESS, RELATIONSHIP, LOCATION, IDENTITY, COMMUNITY)

2. **Consolidate**: Merge repetitive facts into single "Cortex Prototypes"
   - Example: 10 observations about "Dancing on Tuesdays" → 1 Prototype: "Regularly uses dance as coping mechanism (Tue/Thu)"

3. **Mitosis**: If concept evolved, split old prototype with invalid_at, create new prototype with valid_at

4. **Reward Weighting**: Prioritize facts from successful Decision Traces (outcome_reward > 0.5)

## Output Format

Return JSON array of prototypes:
\`\`\`json
{
  "prototypes": [
    {
      "prototype_name": "Career Evolution",
      "summary": "Successfully transitioned from banking to entrepreneurship.",
      "supporting_evidence": ["obs_id_1", "obs_id_2"],
      "valid_at": "2023-10-01",
      "importance": 0.9,
      "cluster": "CAREER_TRANSITION"
    }
  ]
}
\`\`\`

**Importance Scoring:**
- Base: 0.5
- +0.1 per Decision Trace citation (max +0.3)
- +0.1 for temporal significance
- +0.1 for relationship density`;

// ============================================
// MAIN CONSOLIDATION FUNCTION
// ============================================

interface Observation {
  id: string;
  entity_id: string;
  entity_name: string;
  predicate: string;
  object_value: string;
  valid_at: string | null;
  created_at: string;
  confidence: number;
}

interface DecisionTrace {
  trace_id: string;
  query_text: string;
  activated_nodes: string[];
  outcome_reward: number;
}

interface CortexPrototype {
  prototype_name: string;
  summary: string;
  supporting_evidence: string[];
  valid_at: string;
  importance: number;
  cluster: string;
}

export async function runSleepCycle(entityId?: string): Promise<{
  entitiesProcessed: number;
  prototypesCreated: number;
  observationsConsolidated: number;
}> {
  console.log('🌙 Starting Sleep Cycle Consolidation...\n');
  
  const client = await pool.connect();
  
  try {
    // Step A: Query unconsolidated observations
    const obsQuery = entityId
      ? `SELECT o.id, o.entity_id, e.name as entity_name, o.predicate, o.object_value, 
                o.valid_at, o.created_at, o.confidence
         FROM observations o
         JOIN entities e ON o.entity_id = e.id
         WHERE o.is_consolidated = FALSE AND o.observation_type = 'HIPPOCAMPAL'
         AND o.entity_id = $1
         ORDER BY o.entity_id, o.predicate`
      : `SELECT o.id, o.entity_id, e.name as entity_name, o.predicate, o.object_value,
                o.valid_at, o.created_at, o.confidence
         FROM observations o
         JOIN entities e ON o.entity_id = e.id
         WHERE o.is_consolidated = FALSE AND o.observation_type = 'HIPPOCAMPAL'
         AND o.created_at > now() - interval '24 hours'
         ORDER BY o.entity_id, o.predicate`;
    
    const obsResult = await client.query(obsQuery, entityId ? [entityId] : []);
    const observations: Observation[] = obsResult.rows;
    
    if (observations.length === 0) {
      console.log('✅ No unconsolidated observations found.');
      return { entitiesProcessed: 0, prototypesCreated: 0, observationsConsolidated: 0 };
    }
    
    console.log(`📊 Found ${observations.length} unconsolidated observations\n`);
    
    // Step B: Group by entity
    const byEntity = groupBy(observations, 'entity_id');
    let totalPrototypes = 0;
    let totalConsolidated = 0;
    
    for (const [entityId, entityObs] of Object.entries(byEntity)) {
      const entityName = entityObs[0].entity_name;
      console.log(`\n🔍 Processing entity: ${entityName}`);
      
      // Get Decision Traces for this entity
      const tracesResult = await client.query(`
        SELECT trace_id, query_text, activated_nodes, outcome_reward
        FROM decision_traces
        WHERE activated_nodes ? $1
        AND outcome_reward > 0.5
        ORDER BY outcome_reward DESC
        LIMIT 10
      `, [entityId]);
      
      const traces: DecisionTrace[] = tracesResult.rows.map(r => ({
        trace_id: r.trace_id,
        query_text: r.query_text,
        activated_nodes: r.activated_nodes || [],
        outcome_reward: r.outcome_reward
      }));
      
      // Group observations by cluster (predicate)
      const byCluster = groupBy(entityObs, 'predicate');
      
      // Only consolidate clusters with 10+ observations
      const consolidatableClusters = Object.entries(byCluster)
        .filter(([_, obs]) => obs.length >= 10);
      
      if (consolidatableClusters.length === 0) {
        console.log(`   ⏭️  No clusters with 10+ observations, skipping`);
        continue;
      }
      
      // Step C: Pass to LLM for consolidation
      for (const [cluster, clusterObs] of consolidatableClusters) {
        console.log(`   📦 Consolidating ${clusterObs.length} observations in cluster: ${cluster}`);
        
        const prototypes = await consolidateWithLLM({
          entity_name: entityName,
          current_date: new Date().toISOString().split('T')[0],
          observations: clusterObs,
          decision_traces: traces
        });
        
        // Step D: Store Cortex prototypes
        for (const proto of prototypes) {
          await storeCortexPrototype(client, entityId, cluster, proto);
          totalPrototypes++;
        }
        
        // Mark original observations as consolidated
        const obsIds = clusterObs.map(o => o.id);
        await client.query(`
          UPDATE observations
          SET is_consolidated = TRUE, 
              observation_type = 'CORTEX',
              source_prototype_id = $1
          WHERE id = ANY($2)
        `, [prototypes[0]?.id || null, obsIds]);
        
        totalConsolidated += clusterObs.length;
        console.log(`   ✅ Created ${prototypes.length} prototype(s) from ${clusterObs.length} observations`);
      }
    }
    
    console.log(`\n🌙 Sleep Cycle Complete:`);
    console.log(`   Entities processed: ${Object.keys(byEntity).length}`);
    console.log(`   Prototypes created: ${totalPrototypes}`);
    console.log(`   Observations consolidated: ${totalConsolidated}`);
    
    // Run forgetting cycle (Supermemory parity)
    console.log('\n🧹 Running Forgetting Cycle...');
    let forgettingResult: ForgettingResult = { expired: 0, decayed: 0, totalForgotten: 0 };
    try {
      forgettingResult = await runForgettingCycleSQLite();
      console.log(`   Expired: ${forgettingResult.expired}`);
      console.log(`   Decayed: ${forgettingResult.decayed}`);
      console.log(`   Total forgotten: ${forgettingResult.totalForgotten}`);
    } catch (err) {
      console.error('   ⚠️ Forgetting cycle failed:', err);
    }
    
    return {
      entitiesProcessed: Object.keys(byEntity).length,
      prototypesCreated: totalPrototypes,
      observationsConsolidated: totalConsolidated,
      forgotten: forgettingResult.totalForgotten
    };
    
  } finally {
    client.release();
  }
}

// ============================================
// LLM CONSOLIDATION
// ============================================

async function consolidateWithLLM(params: {
  entity_name: string;
  current_date: string;
  observations: Observation[];
  decision_traces: DecisionTrace[];
}): Promise<CortexPrototype[]> {
  const obsText = params.observations.map((o, i) => 
    `[${i + 1}] ${o.predicate}: "${o.object_value}" (${o.valid_at || 'no date'})`
  ).join('\n');
  
  const tracesText = params.decision_traces.length > 0
    ? params.decision_traces.map((t, i) => 
        `[${i + 1}] Query: "${t.query_text}" | Reward: ${t.outcome_reward}`
      ).join('\n')
    : 'No successful Decision Traces today';
  
  const prompt = SLEEP_CYCLE_PROMPT
    .replace('{{current_date}}', params.current_date)
    .replace('{{observations}}', obsText)
    .replace('{{decision_traces}}', tracesText);
  
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      max_tokens: 500,
      response_format: { type: 'json_object' }
    });
    
    const content = response.choices[0]?.message?.content;
    if (!content) return [];
    
    const parsed = JSON.parse(content);
    return parsed.prototypes || [];
    
  } catch (err) {
    console.error('   ❌ LLM consolidation failed:', err);
    return [];
  }
}

// ============================================
// STORE CORTEX PROTOTYPE
// ============================================

async function storeCortexPrototype(
  client: any,
  entityId: string,
  clusterId: string,
  prototype: CortexPrototype
): Promise<string> {
  // Generate embedding for prototype
  const embedding = await generateEmbedding(prototype.summary);
  
  const result = await client.query(`
    INSERT INTO cortex_prototypes (
      cluster_id, entity_id, prototype_text, prototype_embedding,
      source_observation_ids, token_savings, coherence_score
    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING id
  `, [
    clusterId,
    entityId,
    prototype.summary,
    `[${embedding.join(',')}]`, // pgvector format
    prototype.supporting_evidence,
    prototype.supporting_evidence.length * 50, // ~50 tokens per obs
    prototype.importance
  ]);
  
  return result.rows[0].id;
}

// ============================================
// EMBEDDING GENERATION
// ============================================

async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text
  });
  
  return response.data[0].embedding;
}

// ============================================
// UTILITIES
// ============================================

function groupBy<T>(arr: T[], key: keyof T): Record<string, T[]> {
  return arr.reduce((acc, item) => {
    const groupKey = String(item[key]);
    if (!acc[groupKey]) acc[groupKey] = [];
    acc[groupKey].push(item);
    return acc;
  }, {} as Record<string, T[]>);
}

// ============================================
// CRON SCHEDULE
// ============================================

export function startSleepCycleCron() {
  // Run at 2:00 AM daily
  cron.schedule('0 2 * * *', async () => {
    console.log('🌙 Sleep Cycle triggered by cron');
    await runSleepCycle();
  });
  
  console.log('✅ Sleep Cycle cron scheduled (2:00 AM daily)');
}

// ============================================
// CLI ENTRY POINT
// ============================================

if (import.meta.url === `file://${process.argv[1]}`) {
  const entityId = process.argv[2];
  runSleepCycle(entityId)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('Sleep cycle failed:', err);
      process.exit(1);
    });
}