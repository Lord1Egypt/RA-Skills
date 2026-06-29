# Pet Boarding Manager / 宠物寄养管理系统

## Description
A comprehensive pet boarding management system for pet hotels, kennels, and boarding facilities. Manage pet profiles, owner information, reservations, daily care logs, and billing. Supports dogs, cats, and other pets.

宠物寄养管理系统，帮助宠物店、寄养中心高效管理客户、宠物档案、预约、日常护理和费用结算。支持猫、狗等多种宠物。

**Keywords**: pet boarding, pet hotel, kennel management, pet care, 宠物寄养, 宠物店管理, 寄养预约, 宠物护理

## When to use this skill
- User runs a pet boarding business (pet hotel, kennel, cattery)
- Need to track multiple pets and their stay durations
- Need to log daily care activities (feeding, medication, exercise)
- Need to calculate boarding fees based on duration and services
- Want to maintain pet health records and special instructions

## When NOT to use this skill
- User wants to book a boarding service (this is for providers, not customers)
- User needs pet grooming services (use pet-grooming skill instead)
- User wants to find a pet sitter (this is B2B, not B2C)

## How to use this skill

### 1. Register a new pet owner
```
Register a new customer: John Smith, phone +1-555-1234, email john@example.com. His dog Buddy is a 3-year-old Golden Retriever, neutered, weighs 30kg, special instructions: "needs medication after meals".
```

### 2. Create a boarding reservation
```
Create a boarding reservation for Buddy (owner John Smith). Check-in: 2026-06-20, check-out: 2026-06-25. Include premium package (daily walks + grooming).
```

### 3. Log daily care activities
```
Log today's care for Buddy: fed 500g dog food at 8am and 6pm, 30min walk at 9am, medication given after dinner, notes: "ate well, very active".
```

### 4. Calculate boarding fees
```
Calculate total fee for Buddy's stay (2026-06-20 to 2026-06-25, premium package at $45/night). Include 10% tax.
```

### 5. View pet's stay history
```
Show all boarding history for Buddy (pet ID: PET001).
```

### 6. Update pet information
```
Update Buddy's profile: weight changed to 32kg, new special instruction: "now needs joint supplements with meals".
```

## Data Structure

### Pet Owner Profile
```
OwnerID: OWN001
Name: John Smith
Phone: +1-555-1234
Email: john@example.com
Address: 123 Main St, Anytown, USA
Emergency Contact: Jane Smith (wife) +1-555-5678
Created: 2026-06-15
```

### Pet Profile
```
PetID: PET001
Name: Buddy
Species: Dog
Breed: Golden Retriever
Age: 3 years
Gender: Male (neutered)
Weight: 30kg
Vaccination Status: Up-to-date (last: 2026-01-15)
Special Instructions: Needs medication after meals (see meds list)
Medical Conditions: None
OwnerID: OWN001
Created: 2026-06-15
```

### Boarding Reservation
```
ReservationID: RES20250620001
PetID: PET001
CheckIn: 2026-06-20 10:00
CheckOut: 2026-06-25 16:00
Package: Premium ($45/night, includes daily walks + grooming)
Status: Confirmed
TotalNights: 5
Subtotal: $225
Tax: $22.50
Total: $247.50
Notes: "First time boarding, may be anxious"
```

### Daily Care Log
```
LogID: LOG20250621001
PetID: PET001
Date: 2026-06-21
Activities:
  - 08:00: Fed 500g Royal Canin (ate all)
  - 09:00: 30min walk (potty training, pooped normally)
  - 13:00: Medication (antibiotic, after lunch)
  - 18:00: Fed 500g Royal Canin + supplements
  - 19:00: 20min playtime in yard
HealthNotes: "Energetic, good appetite, no diarrhea"
StaffInitials: AS
```

## Pricing Calculator

Base rates (example):
- Standard boarding: $30/night (dogs), $25/night (cats)
- Deluxe boarding: $45/night (dogs), $35/night (cats)
- Luxury suite: $65/night (dogs), $50/night (cats)

Add-on services:
- Extra walk: $10/session
- Grooming: $25/session
- Medication administration: $5/day
- Special diet preparation: $8/day

Tax: 10% (adjustable by location)

## File Storage

All data stored in `~/.openclaw/pet-boarding-data/`:
- `owners.json` - Pet owner profiles
- `pets.json` - Pet profiles
- `reservations.json` - Boarding reservations
- `care-logs.json` - Daily care activity logs
- `billing.json` - Invoices and payment records

## Important Notes

1. **Vaccination required**: Always check vaccination records before confirming reservation
2. **Emergency contacts**: Ensure emergency contact info is complete
3. **Special instructions**: Highlight dietary restrictions, medications, and behavioral issues
4. **Daily logs**: Encourage staff to log detailed care notes (helps with liability)
5. **Photo updates**: Suggest sending daily photos to owners (premium service)

## Example Workflow

**Scenario**: New customer registers and makes reservation

1. User: "I have a new customer, Sarah Johnson. Her cat Luna needs boarding from July 1-5."
2. Assistant: Asks for Sarah's contact info, Luna's details (age, breed, vaccinations)
3. User provides info
4. Assistant: Creates owner profile (OWN002) and pet profile (PET002)
5. Assistant: Checks availability for July 1-5
6. Assistant: Creates reservation (RES20250701002), calculates fee ($25/night x 5 nights = $125 + tax = $137.50)
7. Assistant: Asks if user wants to add grooming service ($25)
8. User: "Yes, add grooming on July 3rd"
9. Assistant: Updates reservation, new total $162.50
10. Assistant: Sends confirmation to customer (email template)

## Troubleshooting

**Q: Pet has diarrhea during stay**
A: Log in health notes, notify owner immediately, offer vet visit if severe. Check if dietary change caused it.

**Q: Owner wants to extend stay**
A: Check availability, update reservation, calculate additional fee, get payment.

**Q: Pet escapes during walk**
A: Emergency protocol: notify owner, search immediately, file incident report, review liability insurance.

**Q: Customer disputes charges**
A: Show detailed care logs, itemized invoice, photos of pet enjoying stay.

## Version
1.0.0 - Initial release
1.0.1 - Added multi-pet support, improved billing calculator

## Author
@katherine0325

## License
MIT
