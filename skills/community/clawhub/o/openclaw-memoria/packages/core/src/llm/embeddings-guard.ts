/**
 * Garde anti-768/1536 (spec §14/§16, port-map embeddings B2) :
 * le legacy retournait cosine=0 sur longueurs différentes → faits invisibles
 * à la recherche sémantique POUR TOUJOURS, sans erreur. Ici on THROW.
 */

/** Vérifie qu'un vecteur a exactement les dimensions promises par son modèle. */
export function assertVectorDimensions(
  vec: Float32Array | ReadonlyArray<number>,
  expected: number,
  model: string,
): void {
  if (vec.length !== expected) {
    throw new Error(
      `dimensions d'embedding invalides pour « ${model} » : reçu ${vec.length}, attendu ${expected} ` +
        `(garde anti-768/1536 — jamais d'écriture cross-dimension)`,
    )
  }
}

/**
 * Similarité cosinus stricte : longueurs différentes = comparaison
 * inter-espaces interdite → erreur (PAS un retour 0 silencieux).
 */
export function cosineSimilarity(a: Float32Array, b: Float32Array): number {
  if (a.length !== b.length) {
    throw new Error(
      `cosineSimilarity : dimensions incompatibles (${a.length} vs ${b.length}) — ` +
        `comparaison inter-espaces d'embedding interdite`,
    )
  }
  if (a.length === 0) {
    throw new Error('cosineSimilarity : vecteurs vides')
  }
  let dot = 0
  let normA = 0
  let normB = 0
  for (let i = 0; i < a.length; i++) {
    const x = a[i]!
    const y = b[i]!
    dot += x * y
    normA += x * x
    normB += y * y
  }
  // Vecteur nul : aucune direction → similarité 0 (cas mathématique, pas une erreur avalée).
  if (normA === 0 || normB === 0) return 0
  return dot / (Math.sqrt(normA) * Math.sqrt(normB))
}
