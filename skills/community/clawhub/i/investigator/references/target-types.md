# Target types

Classify the target before doing anything else.

## Person
Examples:
- full name
- alias
- face / image
- public identity request

Use modules:
- web
- social
- username
- image
- correlation

## Username / Handle
Examples:
- `someuser`
- `@someuser`

Use modules:
- username
- social
- web
- correlation

## Email
Examples:
- `person@example.com`

Use modules:
- email
- web
- breach
- gravatar/public avatar checks

## Domain / Website
Examples:
- `example.com`
- `sub.example.com`

Use modules:
- domain
- dns/whois
- web
- archive

## IP address
Examples:
- `1.2.3.4`

Use modules:
- ip
- dns
- web

## Phone number
Use modules:
- phone
- web
- social

## Organisation / Company
Use modules:
- web
- social
- domain
- maps
- company

## Location / Address
Use modules:
- maps
- geo
- web

## Image
Use modules:
- image
- reverse image search
- metadata when locally available
