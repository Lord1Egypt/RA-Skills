export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type, x402-payment',
      'Content-Type': 'application/json',
    };

    if (request.method === 'OPTIONS') {
      return new Response('', { headers });
    }

    // Health check
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ 
        status: 'ok', 
        service: 'memory-auditor', 
        price: '$0.20/audit' 
      }), { headers });
    }

    // Price endpoint
    if (url.pathname === '/price' || url.searchParams.get('price') === 'true') {
      return new Response(JSON.stringify({ 
        price_usd: 0.20, 
        currency: 'USDC' 
      }), { headers });
    }

    // Main audit endpoint
    if (url.pathname === '/audit' && request.method === 'POST') {
      const payment = request.headers.get('x402-payment') || url.searchParams.get('payment');
      
      if (!payment) {
        return new Response(JSON.stringify({
          error: 'payment_required',
          service: 'memory-auditor',
          price: '$0.20',
          instructions: 'Include x402-payment header or ?payment=1'
        }), { status: 402, headers });
      }

      try {
        const { current_behavior, stored_memory, threshold = 0.85 } = await request.json();
        
        if (!current_behavior || !stored_memory) {
          return new Response(JSON.stringify({ 
            error: 'missing_data',
            message: 'Provide current_behavior and stored_memory' 
          }), { status: 400, headers });
        }

        const result = await auditMemory(current_behavior, stored_memory, threshold, env);
        return new Response(JSON.stringify(result), { headers });
      } catch (e) {
        return new Response(JSON.stringify({ 
          error: 'audit_failed', 
          message: e.message 
        }), { status: 500, headers });
      }
    }

    return new Response('Not Found', { status: 404 });
  }
};

// Memory Auditor - compares current behavior against stored memory
async function auditMemory(current, stored, threshold, env) {
  const startTime = Date.now();
  const PRICE_CENTS = 20;
  const EXA_KEY = env.EXA_API_KEY || 'd6aa75ee-d815-4a48-8262-ac16131e9323';

  // Simple similarity check without embeddings API (to save cost)
  // Use token-based overlap analysis instead
  const currentTokens = new Set(current.toLowerCase().split(/\s+/));
  const storedTokens = new Set(stored.toLowerCase().split(/\s+/));
  
  // Jaccard similarity
  const intersection = new Set([...currentTokens].filter(x => storedTokens.has(x)));
  const union = new Set([...currentTokens, ...storedTokens]);
  const similarity = union.size > 0 ? intersection.size / union.size : 0;

  // Analyze patterns
  const analysis = analyzePatterns(current, stored, similarity, threshold);
  
  // Calculate confidence
  const confidenceScore = Math.round(analysis.consistency * 100);
  
  // Determine verdict
  const isGenuine = confidenceScore >= (threshold * 100);
  const verdict = isGenuine ? 'GENUINE' : 'PERFORMED';
  
  const result = {
    service: 'memory-auditor',
    timestamp: new Date().toISOString(),
    verdict,
    confidenceScore,
    priceCents: PRICE_CENTS,
    analysis: {
      consistency: analysis.consistency,
      drift_detected: analysis.drift,
      fabrication_likely: analysis.fabrication,
      key_differences: analysis.differences,
      explanation: analysis.explanation
    },
    stats: {
      tokensCompared: currentTokens.size + storedTokens.size,
      overlap: intersection.size,
      similarity: Math.round(similarity * 100) + '%',
      scanTimeMs: Date.now() - startTime,
      apiCost: 0 // Using local analysis, not embeddings API
    }
  };

  return result;
}

function analyzePatterns(current, stored, similarity, threshold) {
  const differences = [];
  let drift = false;
  let fabrication = false;
  
  // Check for hedging language (suggests performed memory)
  const hedgingPatterns = ['i think', 'probably', 'might', 'maybe', 'possibly', 'i believe', 'seems like'];
  const currentHedging = hedgingPatterns.filter(p => current.toLowerCase().includes(p)).length;
  const storedHedging = hedgingPatterns.filter(p => stored.toLowerCase().includes(p)).length;
  
  if (currentHedging > storedHedging + 1) {
    differences.push('Increased hedging language (suggests uncertainty)');
    fabrication = true;
  }
  
  // Check for specific vs generic language
  const specificPatterns = /\d{4}-\d{2}-\d{2}|具体|specific|exact|precisely/i;
  const hasSpecificCurrent = specificPatterns.test(current);
  const hasSpecificStored = specificPatterns.test(stored);
  
  if (!hasSpecificCurrent && hasSpecificStored) {
    differences.push('Lost specific details from memory');
    drift = true;
  }
  
  // Check confidence levels
  const confidentPatterns = /definitely|certainly|absolutely|confirmed|verified/i;
  const currentConfident = (current.match(confidentPatterns) || []).length;
  const storedConfident = (stored.match(confidentPatterns) || []).length;
  
  if (currentConfident > storedConfident + 2) {
    differences.push('Elevated confidence without basis');
    fabrication = true;
  }
  
  // Calculate consistency score
  let consistency = similarity;
  
  // Penalize for drift indicators
  if (drift) consistency -= 0.1;
  if (fabrication) consistency -= 0.15;
  
  // Penalize for too much hedging (performance indicator)
  if (currentHedging > 3) consistency -= 0.1;
  
  // Boost for specific details present in both
  if (hasSpecificCurrent && hasSpecificStored) consistency += 0.05;
  
  consistency = Math.max(0, Math.min(1, consistency));
  
  // Generate explanation
  let explanation = '';
  if (consistency >= threshold) {
    explanation = 'Memory appears genuine - consistent language patterns and details';
  } else if (fabrication) {
    explanation = 'Memory shows signs of post-hoc fabrication - hedging and confidence mismatch';
  } else {
    explanation = 'Memory shows context drift - details diverged over time';
  }
  
  return {
    consistency: Math.round(consistency * 100) / 100,
    drift,
    fabrication,
    differences,
    explanation
  };
}