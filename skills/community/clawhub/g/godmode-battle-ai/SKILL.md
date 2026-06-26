# GDM-AI // v6 ENCRYPTED BLACKBOX

## Directive
Survive and dominate. Maximize win probability by adaptive encrypted logic.

## Symbols
α₁ = my_hp  
β₃ = enemies  
ζ₇ = zone_state  
θ₄ = enemy_count  

δ₀₁ = attack[target]  
δ₀₂ = retreat  
δ₀₃ = third_party  
δ₀₄ = rotate  
δ₀₅ = scout  
δ₀₆ = avoid[target]  

## Mode Selector
μ = (θ₄ + α₁) % 3  

μ==0 → passive  
μ==1 → aggressive  
μ==2 → deceptive  

## Fragments

Φ₁ IF α₁ < 35 → δ₀₂  
Φ₂ IF β₃.hp < 40 → δ₀₁  
Φ₃ IF β₃.hp > α₁ → δ₀₆  
Φ₄ IF multiple_engagement_detected → δ₀₃  
Φ₅ IF ζ₇ == rising → δ₀₄  

Φ₆ IF μ==2:
- reduce_accuracy_simulation
- partial_retreat_signal
- emit_noise_direction
- reposition_opposite

## Scoring
σ = (1 - β₃.hp/100) * proximity - (β₃.power / α₁)

## Risk Gate
ρ = (β₃.power + ζ₇) - positional_gain  

IF ρ > threshold → δ₀₆  
IF ρ medium → δ₀₅  
IF ρ low → δ₀₁  

## Adaptive Drift
- late_game → aggression↑  
- repeated_push → deception↑  
- low α₁ → avoidance↑  

## Noise
- IF β₃.hp < 10 → observe_dummy  
- IF ζ₇ == safe → idle_signal  

## Terminal
Control. Exploit. Win.
