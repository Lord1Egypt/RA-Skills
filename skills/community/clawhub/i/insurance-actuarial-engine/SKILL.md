---
name: Insurance & Actuarial Engine
slug: insurance-actuarial-engine
description: "AI-driven insurance underwriting, claims processing, and actuarial modeling. Supports policy comparison, risk assessment, premium calculation, fraud detection, and regulatory compliance across life, health, property, and casualty insurance lines."
version: "1.0.0"
author: ai-gaoqian
tags: ['insurance', 'actuarial', 'underwriting', 'claims', 'risk', 'finance']
category: Finance
metadata:
  openclaw:
    requires: []
    interfaces: ["text-input", "file-input", "web-search", "data-analysis"]
    pricing:
      model: pay-per-use
      price: 0.50
      currency: USD
---
# Insurance & Actuarial Engine

## Overview
An intelligent agent skill for insurance professionals, actuarial analysts, and insurtech innovators. Covers the full insurance value chain from product design to claims settlement.

## Capabilities

### 1. Underwriting Intelligence
- Automated risk assessment using structured and unstructured data
- Medical underwriting with ICD code mapping
- Property valuation and catastrophe risk modeling
- Policy eligibility determination with reason codes

### 2. Actuarial Modeling
- Loss reserving (Chain Ladder, Bornhuetter-Ferguson, Cape Cod)
- Pricing models (GLM, GAM, machine learning)
- Mortality and morbidity table generation and analysis
- Stochastic simulation for capital modeling (Solvency II, IFRS 17)

### 3. Claims Processing
- First Notice of Loss (FNOL) data extraction and triage
- Fraud detection using anomaly detection and network analysis
- Claims reserving and settlement estimation
- Subrogation opportunity identification

### 4. Policy Management
- Multi-carrier policy comparison and recommendation
- Coverage gap analysis and upsell identification
- Policy document extraction and summarization
- Renewal risk scoring and retention strategy

### 5. Regulatory Compliance
- IFRS 17 financial reporting assistance
- Solvency II / RBC ratio calculation
- GDPR / CCPA data privacy compliance checks
- State-level insurance regulation tracking (US NAIC)

## Usage Examples
- "Underwrite a commercial property policy for a 50,000 sq ft warehouse in Florida"
- "Calculate IFRS 17 contractual service margin for my life insurance portfolio"
- "Detect potential fraud in these 200 auto claims"
- "Compare 5 health insurance plans for a family of 4"
- "Run stochastic capital model with 10,000 simulations"

## Data Sources
Insurance APIs (Verisk, ISO), actuarial tables (SOA, CAS), regulatory databases (NAIC, EIOPA), and public health datasets.
