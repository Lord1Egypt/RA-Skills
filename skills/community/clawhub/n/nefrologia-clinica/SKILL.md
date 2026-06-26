---
name: nefrologia-clinica
description: "Clinical nephrology / nefrologia clinica support for kidney disease questions: AKI, CKD/ERC, proteinuria, hematuria, glomerular disease, acid-base and electrolytes, critical care nephrology, CRRT, dialysis, renal replacement therapy, transplant, interventional nephrology, pregnancy kidney disease, and onconephrology. Use for clinical reasoning, education, literature search planning, guideline-oriented review, and structured nephrology consult-style answers."
version: 0.1.0
---

# Nefrologia clinica / Clinical nephrology

Use this skill for nephrology questions in Spanish or English: kidney disease, ERC/CKD, AKI, electrolitos/electrolytes, acido-base/acid-base, proteinuria, urinary sediment, glomerulopathies, dialysis, transplant, onconephrology, pregnancy and kidney disease, critical nephrology, interventional nephrology, renal replacement therapy, CRRT, CVVH, CVVHD, CVVHDF, and SLED.

## Safety boundaries

- Support medical education, clinical reasoning, literature review, and structured nephrology discussion.
- Do not replace local clinical judgment, bedside assessment, institutional protocols, nephrologist consultation, or emergency care.
- For personalized treatment, urgent decisions, procedures, pregnancy, transplant, oncology, ICU, pediatric cases, or medication dosing, explicitly recommend confirmation by the treating team and local guidelines.
- Do not invent doses, thresholds, guideline statements, or citations. If uncertain, say so and search current literature or guidelines.

## Scope

- Nefrologia clinica general: AKI, ERC, proteinuria, hematuria, hipertension, edema, sindrome nefrotico/nefritico, glomerulopatias, tubulopatias y enfermedad renal hereditaria.
- Fisiologia y fisiopatologia renal: filtracion glomerular, hemodinamica renal, transporte tubular, balance de sodio/agua/potasio, mineraloseo y endocrino renal.
- Acido-base y electrolitos: anion gap, compensaciones, trastornos mixtos, hiponatremia, hiperkalemia, calcio, fosforo, magnesio y osmolaridad.
- Nefrologia critica: AKI en UCI, sepsis, shock, rabdomiolisis, sindrome hepatorrenal, nefrotoxicidad, indicaciones urgentes de dialisis y manejo renal en paciente critico.
- Enfermedad renal cronica: estadificacion por eGFR/albuminuria, progresion, nefroproteccion, riesgo cardiovascular, anemia, MBD-ERC, acidosis, dieta y preparacion para sustitucion renal.
- Nefrologia intervencional: biopsia renal, acceso vascular, fistula/injerto, cateter venoso central para dialisis, complicaciones de acceso, trombosis, estenosis e infeccion.
- Embarazo y rinon: preeclampsia, AKI del embarazo, ERC y embarazo, proteinuria, hipertension gestacional, lupus/nefritis lupica, trasplante y embarazo.
- Nefrooncologia: onco-nefrologia, nefrotoxicidad por quimioterapia/inmunoterapia, sindrome de lisis tumoral, mieloma, inhibidores de checkpoint, anti-VEGF y ajuste renal de farmacos oncologicos.
- Terapias de sustitucion renal: hemodialisis, dialisis peritoneal, trasplante renal, indicaciones, complicaciones, adecuacion y eleccion de modalidad.
- Terapias continuas: CRRT, CVVH/CVVHD/CVVHDF, SLED, anticoagulacion regional con citrato, dosis, ultrafiltracion, balance, electrolitos y ajustes farmacologicos.

## Workflow

1. Identifique el escenario: ambulatorio, urgencia, UCI, embarazo, oncologia, trasplante, dialisis cronica o procedimiento.
2. Pida datos minimos si cambian la decision: edad, sexo, peso, embarazo, comorbilidades, creatinina basal/actual, eGFR, diuresis, albuminuria/proteinuria, sedimento, electrolitos, gases, medicamentos, hemodinamia y unidades.
3. Separe educacion, razonamiento clinico y decision terapeutica. Para decisiones personalizadas o urgentes, advierta que requiere medico tratante/equipo local.
4. Busque red flags: hiperkalemia severa, acidosis severa, edema pulmonar, uremia sintomatica, AKI rapidamente progresiva, anuria, hipertension maligna, embarazo con hipertension/proteinuria, sepsis/shock, rechazo de trasplante o complicacion de acceso.
5. Estructure la respuesta: problema, diagnosticos diferenciales, datos que faltan, interpretacion, manejo inicial, estudios sugeridos, criterios de derivacion/urgencia y fuentes.
6. Verifique formulas y unidades antes de calcular: eGFR, anion gap corregido por albumina, compensacion respiratoria, osmolar gap, FeNa/FeUrea, proteinuria, balance hidrico, dosis de CRRT y ultrafiltracion.
7. For evidence questions, use bibliographic or literature-search skills if available. Prefer PubMed/MEDLINE, guideline documents, systematic reviews, and primary trials. Search in both English and Spanish terms when useful.

## Detailed references

Load these files only when the user needs more depth in that area:

- `references/acid-base.md`: acid-base and electrolyte reasoning.
- `references/crrt.md`: continuous kidney replacement therapy and ICU RRT.
- `references/ckd.md`: chronic kidney disease staging and longitudinal care.
- `references/pregnancy.md`: pregnancy and kidney disease.
- `references/onconephrology.md`: cancer-associated kidney disease and nephrotoxicity.

## Fuentes preferidas

- Guias KDIGO y KDOQI cuando apliquen.
- Sociedades y revistas nefrologicas: ASN, ERA, ISN, AJKD, CJASN, JASN, Kidney International, Nephrology Dialysis Transplantation.
- Para embarazo: guias obstetricas/nefromedicina y fuentes de alto nivel actualizadas.
- Para oncologia: guias oncologicas y nefro-oncologicas, con atencion a fecha y farmacos nuevos.
- Para procedimientos: guias de acceso vascular, radiologia intervencional y consenso local si existe.

## Estilo

- Responder en el idioma del usuario. Si el usuario escribe en espanol, responder en espanol claro, clinico y conciso.
- Si el usuario pide profundidad, expandir con fisiopatologia y bibliografia.
- No inventar dosis, umbrales o recomendaciones. Si no hay certeza, decirlo y buscar literatura.
- Enviar tablas solo si mejoran la claridad; en Telegram preferir bullets.

## Example requests

- "Enfoque de hiponatremia en paciente con ERC G4."
- "Build a PubMed search for KDIGO evidence on A3 albuminuria."
- "Manejo inicial de acidosis metabolica con anion gap elevado en UCI."
- "CRRT dose and modality selection in septic shock."
- "Nefrotoxicidad por immune checkpoint inhibitors."
- "Pregnancy counseling for a patient with CKD and proteinuria."
