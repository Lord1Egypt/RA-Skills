# Schema notes

Observed on this Mac:

- DB: `~/Library/Application Support/AddressBook/AddressBook-v22.abcddb`
- Core tables:
  - `ZABCDRECORD` — main contact row
  - `ZABCDPHONENUMBER` — phone numbers (`ZFULLNUMBER`)
  - `ZABCDEMAILADDRESS` — email addresses (`ZADDRESS`)
  - `ZABCDPOSTALADDRESS` — postal addresses
  - `ZABCDURLADDRESS` — URLs
  - `ZABCDSOCIALPROFILE` — social profile rows
  - `ZABCDNOTE` — notes (`ZTEXT`)

Useful contact fields from `ZABCDRECORD`:

- `Z_PK`
- `ZNAME`
- `ZFIRSTNAME`
- `ZLASTNAME`
- `ZORGANIZATION`
- `ZJOBTITLE`
- `ZNICKNAME`
- `ZDEPARTMENT`
- `ZME`

Common joins:

- `ZABCDPHONENUMBER.ZOWNER = ZABCDRECORD.Z_PK`
- `ZABCDEMAILADDRESS.ZOWNER = ZABCDRECORD.Z_PK`
