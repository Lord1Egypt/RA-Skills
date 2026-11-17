# Worked Example

This example shows how to use the MiroFish skill without any backend.

## Scenario

Seed material:

> A city is considering a draft policy that limits late-night delivery in dense residential districts.

Prediction requirement:

> Predict how residents, delivery platforms, small restaurants, and regulators may react over the next 30 days.

Additional context:

> Focus on public opinion, platform adaptation, and policy rollback risk.

## 1. Scenario Summary

The policy introduces friction between convenience, noise reduction, platform revenue, and regulatory credibility. The important question is not whether people approve in the abstract, but whether specific incentives push the policy toward enforcement, adaptation, or rollback.

## 2. Ontology Sketch

- `Resident`: wants less noise, faster service, or both
- `DeliveryPlatform`: wants to preserve volume and market share
- `Restaurant`: wants to keep orders flowing without raising costs
- `Regulator`: wants visible enforcement without backlash

Relations:

- `Resident` opposes `DeliveryPlatform` when noise rises
- `Restaurant` depends_on `DeliveryPlatform` for demand
- `Regulator` influences `DeliveryPlatform` through enforcement risk
- `PolicyDraft` blocks late-night delivery in dense districts

## 3. Simulation Plan

- agent scale: 4-8 actors plus a few local subtypes
- memory: recent complaints, order volume, enforcement signals, media reactions
- conflicts: convenience vs noise reduction, revenue vs compliance, credibility vs backlash
- branch drivers: enforcement intensity, platform workarounds, restaurant resistance
- stop condition: policy stabilizes, softens, or faces rollback pressure

## 4. Forecast Brief

Most likely path: the policy is partially enforced, platforms adapt with routing or timing changes, restaurants absorb some friction, and public opinion splits between residents who notice improvement and users who dislike delays.

Alternative branches:

- weak enforcement leads to symbolic compliance only
- stronger backlash pushes a policy revision or rollback
- platform adaptation reduces the policy's visible impact

## 5. Interview Questions

- What would make you support or oppose the policy more strongly?
- Which constraint would force you to change behavior?
- What workaround would you try first?
- What public statement would differ from your private incentive?

## 6. Revision Rule

If interviews show that enforcement is weaker than expected, shift the forecast toward symbolic compliance. If residents remain mobilized despite platform workarounds, raise rollback risk.
