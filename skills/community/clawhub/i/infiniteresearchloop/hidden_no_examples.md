# Hidden NO Examples

This document provides real-world examples of Hidden NOs and how to detect them.

## Example 1: Unsupported Claim (Severity 2)

**Scenario:** A user asks for the best machine learning framework for production systems.

**Initial Reasoning:** "TensorFlow is the best framework because it's widely used."

**Hidden NO Detected:** The claim "best" is unsupported. "Widely used" does not mean "best for production." Different frameworks excel in different contexts.

**Refined Reasoning:** "TensorFlow is widely used in production, but the best framework depends on your specific needs. PyTorch excels in research, TensorFlow in deployment, and JAX in numerical computing. Consider your use case before deciding."

**Severity:** 2 (meaningful issue requiring refinement)

## Example 2: Weak Sourcing (Severity 2)

**Scenario:** A user asks about the latest trends in AI safety.

**Initial Reasoning:** "According to a blog post I remember, AI safety is becoming more important."

**Hidden NO Detected:** Vague sourcing ("a blog post I remember") is weak. The information may be outdated or from an unreliable source.

**Refined Reasoning:** Research recent publications from established AI safety organizations (OpenAI, DeepMind, Center for AI Safety) to provide evidence-based trends.

**Severity:** 2 (meaningful issue requiring research)

## Example 3: Contradiction (Severity 3)

**Scenario:** A user asks whether a certain chemical is safe for food.

**Initial Reasoning:** "The chemical is safe because it's been approved by regulatory bodies. However, some studies show it causes health issues."

**Hidden NO Detected:** These statements contradict each other. Approval doesn't guarantee safety if credible studies show harm.

**Refined Reasoning:** Research both regulatory approval and independent studies. Synthesize findings by explaining different approval standards, study methodologies, and risk assessments.

**Severity:** 3 (major blocker requiring deeper research)

## Example 4: Misunderstood Intent (Severity 3)

**Scenario:** A user asks, "Should I invest in cryptocurrency?"

**Initial Reasoning:** "Yes, cryptocurrency is a good investment because it has high returns."

**Hidden NO Detected:** The user's intent is unclear. Are they asking about risk tolerance, portfolio diversification, market timing, or specific cryptocurrencies? Recommending investment without understanding their situation is risky.

**Refined Reasoning:** Ask clarifying questions about their financial goals, risk tolerance, investment horizon, and existing portfolio before providing recommendations.

**Severity:** 3 (major blocker requiring clarification)

## Example 5: Shallow Analysis (Severity 2)

**Scenario:** A user asks for the benefits of remote work.

**Initial Reasoning:** "Remote work is good because people can work from anywhere."

**Hidden NO Detected:** The analysis is shallow. It doesn't consider trade-offs, context, or different perspectives.

**Refined Reasoning:** Remote work has benefits (flexibility, reduced commute, cost savings) and drawbacks (isolation, collaboration challenges, timezone complexity). The effectiveness depends on job type, company culture, and individual preferences.

**Severity:** 2 (meaningful issue requiring deeper synthesis)

## Example 6: False Certainty (Severity 2)

**Scenario:** A user asks about the future of a specific technology.

**Initial Reasoning:** "Blockchain will definitely revolutionize finance in the next 5 years."

**Hidden NO Detected:** Predicting the future with certainty is unreliable. Many factors influence technology adoption.

**Refined Reasoning:** "Blockchain has potential to impact finance, but adoption faces regulatory, technical, and adoption challenges. Timeline and impact remain uncertain."

**Severity:** 2 (meaningful issue requiring uncertainty acknowledgment)

## Example 7: Outdated Information (Severity 2)

**Scenario:** A user asks about the latest Python version.

**Initial Reasoning:** "Python 3.8 is the latest version."

**Hidden NO Detected:** This information is outdated. Python has released newer versions.

**Refined Reasoning:** Research current Python versions and provide up-to-date information with release dates.

**Severity:** 2 (meaningful issue requiring research)

## Example 8: Missing Perspective (Severity 1)

**Scenario:** A user asks about the pros and cons of a policy.

**Initial Reasoning:** "The policy is good because it increases efficiency."

**Hidden NO Detected:** Only one perspective is presented. Other stakeholders may have different views.

**Refined Reasoning:** Present multiple perspectives (business, employee, customer, regulatory) to provide balanced analysis.

**Severity:** 1 (minor weakness; can finalize if stable, but better with refinement)

## Detection Patterns

| Hidden NO Type | Detection Pattern | Typical Severity |
| --- | --- | --- |
| Contradiction | Statements conflict with each other | 3 |
| Unsupported Claim | Conclusion without evidence | 2 |
| Weak Sourcing | Vague or unreliable sources | 2 |
| Misunderstood Intent | User's true goal is unclear | 3 |
| Shallow Analysis | Lacks depth or nuance | 2 |
| False Certainty | Predicts future with certainty | 2 |
| Outdated Information | Information is no longer current | 2 |
| Missing Perspective | Important viewpoints omitted | 1 |
| Logical Fallacy | Reasoning violates logic | 2-3 |
| Incomplete Verification | Key facts not verified | 2 |

## How to Detect Hidden NOs

1. **Ask critical questions** - Does this claim have evidence? Is this information current? Are there contradictions?
2. **Compare perspectives** - What would someone with a different viewpoint say?
3. **Test assumptions** - Are assumptions justified? What if they're wrong?
4. **Verify sources** - Are sources reliable, recent, and authoritative?
5. **Check for gaps** - What important information is missing?
6. **Assess confidence** - Can I defend this conclusion if challenged?
