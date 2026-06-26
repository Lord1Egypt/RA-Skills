# FAERS Fields Reference (openFDA Drug Event API)

## Core Report Fields
- `safetyreportid`: Unique ID
- `receivedate`: Report received date (YYYYMMDD)
- `receiptdate`: Initial receipt date
- `serious`: 1 if serious
- `seriousnessdeath`: 1 if death
- `transmissiondate`: Transmission date

## Primary Source
- `primarysource.reportercountry`: Country
- `primarysource.qualification`: Qualification code

## Patient
- `patient.patientonsetage`: Age at onset
- `patient.patientonsetageunit`: Unit (801=year)
- `patientsex`: 1=Male, 2=Female
- `patientdeath.patientdeathdate`: Death date

## Reactions (array)
- `patient.reaction.reactionmeddrapt`: Preferred Term (PT)
- `patient.reaction.reactionmeddrasoc`: System Organ Class (SOC)

## Drugs (array)
- `patient.drug.medicinalproduct`: Generic name
- `patient.drug.drugcharacterization`: 1=Suspect Single, 2=Concomitant
- `patient.drug.openfda.brand_name`: Brand name
- `patient.drug.openfda.manufacturer_name`
- `patient.drug.drugadministrationroute`: Route code
- `patient.drug.drugindication`: Indication

## Outcomes (array)
- `patient.outcome.result`: 1=Fatal, 2=Hospitalized, etc.

## Search Examples
- Drug: `patient.drug.medicinalproduct:\"aspirin\"`
- Brand: `patient.drug.openfda.brand_name:\"Bayer Aspirin\"`
- Reaction: `patient.reaction.reactionmeddrapt:\"NAUSEA\"`
- Year: `receivedate:[20040101 TO 20260101]`

## Count Endpoints
Use `&count=receivedate` for yearly trends (parse year from date).
`&count=patient.reaction.reactionmeddrapt` for top reactions.

More fields: https://open.fda.gov/apis/drug/event/