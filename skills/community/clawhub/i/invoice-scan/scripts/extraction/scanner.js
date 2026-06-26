/**
 * Invoice Scanner — Core Extraction Engine
 * 
 * Orchestrates the full pipeline:
 * 1. Detect file type
 * 2. Pre-process image
 * 3. Send to AI provider
 * 4. Normalise response via adapter
 * 5. Validate
 * 6. Return canonical invoice
 */

const fs = require('fs');
const path = require('path');
const { preprocessImage, detectFileType } = require('../preprocessing/preprocess');
const { getAdapter, listProviders } = require('../adapters/index');
const { validateArithmetic } = require('../validation/arithmetic');
const { validateDocumentRules } = require('../validation/document-rules');
const { validateSchema } = require('../schema/canonical');
const { checkCompleteness, getRetryFields, buildRetryPrompt, mergeRetryResults } = require('../validation/completeness');

/**
 * Scan an invoice document.
 * 
 * @param {string} filePath - Path to the invoice file
 * @param {object} options
 * @param {string} options.provider - AI provider name (default: 'claude')
 * @param {string} options.apiKey - API key for the provider
 * @param {string} options.model - Model name override
 * @param {boolean} options.preprocess - Run pre-processing (default: true)
 * @param {string} options.apiBaseUrl - Custom API base URL
 * @returns {Promise<object>} Canonical invoice object
 */
async function scanInvoice(filePath, options = {}) {
  const {
    provider = 'claude',
    apiKey,
    model,
    preprocess = true,
    apiBaseUrl,
    retryMissing = true,       // Enable completeness retry pass
    // Document type filtering
    // 'strict' = only invoice + credit-note
    // 'relaxed' = also accept receipt, other-financial (proforma, etc.)
    // 'any' = extract from anything, just classify it
    acceptTypes = 'relaxed',
  } = options;

  const startTime = Date.now();

  // Validate inputs
  if (!filePath) throw new Error('filePath is required');
  if (!fs.existsSync(filePath)) throw new Error(`File not found: ${filePath}`);
  if (!apiKey) throw new Error('apiKey is required. Set via options or ANTHROPIC_API_KEY env var.');

  const fileType = detectFileType(filePath);
  if (fileType === 'unknown') {
    throw new Error(`Unsupported file type: ${path.extname(filePath)}`);
  }

  // Step 1: Read file
  let imageBuffer = fs.readFileSync(filePath);
  let preprocessMeta = { preprocessed: false };

  // Step 2: Pre-process (images only, not native PDFs for now)
  if (preprocess && fileType === 'image') {
    const result = await preprocessImage(imageBuffer);
    imageBuffer = result.buffer;
    preprocessMeta = result.metadata;
  }

  // Step 3: Get adapter and build prompt
  const adapter = getAdapter(provider);
  const prompt = adapter.buildPrompt();

  // Step 4: Call AI provider
  const rawResponse = await callProvider(provider, {
    imageBuffer,
    prompt,
    apiKey,
    model,
    apiBaseUrl,
    filePath,
  });

  // Step 5: Normalise response
  const invoice = adapter.normalise(rawResponse);

  // Step 6: Validate
  validateArithmetic(invoice);
  validateDocumentRules(invoice);

  // Step 7: Schema validation
  const schemaResult = validateSchema(invoice);
  if (!schemaResult.valid) {
    for (const err of schemaResult.errors) {
      invoice.validation.warnings.push({
        field: 'schema',
        message: err,
      });
    }
  }

  // Step 8: Completeness check + retry for missing fields
  const completenessReport = checkCompleteness(invoice);
  invoice.metadata.completeness = {
    score: completenessReport.score,
    populated: completenessReport.populated,
    missing: completenessReport.missing,
    notOnDocument: completenessReport.notOnDocument,
    retried: false,
    retryRecovered: 0,
    retryConfirmedAbsent: 0,
  };

  if (retryMissing && completenessReport.missing > 0) {
    const retryFields = getRetryFields(invoice);
    if (retryFields.length > 0) {
      try {
        const retryPrompt = buildRetryPrompt(retryFields);
        const retryResponse = await callProvider(provider, {
          imageBuffer,
          prompt: retryPrompt,
          apiKey,
          model,
          apiBaseUrl,
          filePath,
        });

        if (retryResponse.retryFields && Array.isArray(retryResponse.retryFields)) {
          const mergeSummary = mergeRetryResults(invoice, retryResponse.retryFields);
          invoice.metadata.completeness.retried = true;
          invoice.metadata.completeness.retryRecovered = mergeSummary.recovered.length;
          invoice.metadata.completeness.retryConfirmedAbsent = mergeSummary.confirmedAbsent.length;

          // Log recovered fields as warnings for visibility
          for (const r of mergeSummary.recovered) {
            invoice.validation.warnings.push({
              field: r.path,
              message: `Recovered on retry pass: ${JSON.stringify(r.value)}`,
            });
          }
          for (const a of mergeSummary.confirmedAbsent) {
            invoice.validation.warnings.push({
              field: a.path,
              message: `Confirmed not on document: ${a.reason || 'no reason given'}`,
            });
          }

          // Re-run validators after merge
          invoice.validation.arithmeticValid = null;
          validateArithmetic(invoice);
          validateDocumentRules(invoice);
        }
      } catch (retryErr) {
        invoice.validation.warnings.push({
          field: 'completeness',
          message: `Retry pass failed: ${retryErr.message}`,
        });
      }

      // Recompute completeness after retry
      const postRetry = checkCompleteness(invoice);
      invoice.metadata.completeness.score = postRetry.score;
      invoice.metadata.completeness.populated = postRetry.populated;
      invoice.metadata.completeness.missing = postRetry.missing;
      invoice.metadata.completeness.notOnDocument += postRetry.notOnDocument;
    }
  }

  // Step 9: Populate metadata
  invoice.metadata.processingDurationMs = Date.now() - startTime;
  invoice.metadata.pageCount = 1; // TODO: multi-page support

  // Determine overall status
  const hasErrors = invoice.validation.errors.length > 0;
  const hasCriticalMissing = !invoice.header.invoiceNumber && !invoice.header.supplierName;
  const docType = invoice.metadata.documentType;
  const strictTypes = ['invoice', 'credit-note'];
  const relaxedTypes = [...strictTypes, 'receipt', 'other-financial'];
  const acceptedTypes = acceptTypes === 'any' ? null 
    : acceptTypes === 'relaxed' ? relaxedTypes 
    : strictTypes;
  const isAccepted = !docType || !acceptedTypes || acceptedTypes.includes(docType);

  if (!isAccepted) {
    invoice.exceptions.overallStatus = 'rejected';
    invoice.exceptions.rejectionReason = `Document is "${docType}", not an accepted type (mode: ${acceptTypes})`;
  } else if (hasCriticalMissing) {
    invoice.exceptions.overallStatus = 'failed';
  } else if (hasErrors) {
    invoice.exceptions.overallStatus = 'partial';
  } else {
    invoice.exceptions.overallStatus = 'success';
  }

  return invoice;
}

/**
 * Call the AI provider API.
 * Currently supports Claude (Anthropic).
 */
async function callProvider(provider, { imageBuffer, prompt, apiKey, model, apiBaseUrl, filePath }) {
  if (provider === 'claude') {
    return await callClaude({ imageBuffer, prompt, apiKey, model, apiBaseUrl, filePath });
  }
  throw new Error(`Provider "${provider}" API call not implemented yet`);
}

/**
 * Call Claude's Messages API with vision.
 */
async function callClaude({ imageBuffer, prompt, apiKey, model, apiBaseUrl, filePath }) {
  const baseUrl = apiBaseUrl || 'https://api.anthropic.com';
  const modelName = model || 'claude-sonnet-4-20250514';

  // Detect actual media type from file magic bytes (not extension — files often lie)
  const magic = imageBuffer.slice(0, 8);
  let mediaType = 'image/png'; // default
  if (magic[0] === 0x89 && magic[1] === 0x50 && magic[2] === 0x4E && magic[3] === 0x47) {
    mediaType = 'image/png';
  } else if (magic[0] === 0xFF && magic[1] === 0xD8 && magic[2] === 0xFF) {
    mediaType = 'image/jpeg';
  } else if (magic[0] === 0x47 && magic[1] === 0x49 && magic[2] === 0x46) {
    mediaType = 'image/gif';
  } else if (magic[0] === 0x52 && magic[1] === 0x49 && magic[2] === 0x46 && magic[3] === 0x46) {
    mediaType = 'image/webp';
  } else if (magic[0] === 0x25 && magic[1] === 0x50 && magic[2] === 0x44 && magic[3] === 0x46) {
    mediaType = 'application/pdf';
  }

  const base64Image = imageBuffer.toString('base64');

  const body = {
    model: modelName,
    max_tokens: 4096,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'image',
            source: {
              type: 'base64',
              media_type: mediaType,
              data: base64Image,
            },
          },
          {
            type: 'text',
            text: prompt,
          },
        ],
      },
    ],
  };

  // Support both direct API keys (sk-ant-api...) and OAuth tokens (sk-ant-oat...)
  const headers = {
    'Content-Type': 'application/json',
    'anthropic-version': '2023-06-01',
  };
  if (apiKey.startsWith('sk-ant-oat')) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  } else {
    headers['x-api-key'] = apiKey;
  }

  const response = await fetch(`${baseUrl}/v1/messages`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Claude API error (${response.status}): ${errText}`);
  }

  const result = await response.json();

  // Extract JSON from Claude's response text
  const textContent = result.content?.find(c => c.type === 'text');
  if (!textContent) {
    throw new Error('No text content in Claude response');
  }

  // Parse JSON — handle potential markdown wrapping
  let jsonStr = textContent.text.trim();
  if (jsonStr.startsWith('```')) {
    jsonStr = jsonStr.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '');
  }

  try {
    return JSON.parse(jsonStr);
  } catch (e) {
    throw new Error(`Failed to parse Claude response as JSON: ${e.message}\nRaw: ${jsonStr.substring(0, 500)}`);
  }
}

module.exports = { scanInvoice };
