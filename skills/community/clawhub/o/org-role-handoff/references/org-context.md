# Organization Context

This skill is based on the target organization structure, which combines executive leadership, IT leadership, operational leadership, and supporting functional roles.

## Top-level structure

- Executive Director
  - IT Director
    - Information Technology Manager
      - Quality Assurance
      - Database Administrator
        - Web Developer
        - Mobile Developer
  - Operational Director
    - Product & Project Manager
      - UI/UX Designer
        - Graphic Designer
      - Product Designer
      - Business Analyst
  - General Administration

## Organizational interpretation

This structure reflects a company where executive leadership oversees both IT and operational functions.

- The Executive Director holds overall business oversight and strategic direction.
- The IT Director oversees IT strategy, information systems, security, compliance, and high-level technology governance.
- The Operational Director oversees daily operations, resource allocation, process improvement, and operational performance.
- The Information Technology Manager coordinates execution inside the IT function and manages communication between IT and other departments.
- The Product & Project Manager coordinates project lifecycle, product direction, and cross-functional execution between business, design, and development-related functions.
- General Administration supports general administrative and operational management work across the company.

## IT-side interpretation

The IT branch includes roles responsible for system implementation, technical execution, and product quality.

- Quality Assurance focuses on testing and quality validation.
- Database Administrator focuses on database availability, integrity, security, and performance.
- Web Developer focuses on website development and maintenance.
- Mobile Developer focuses on mobile application development and maintenance.

## Operations and product-side interpretation

The operations branch includes planning, design, business understanding, and coordination roles.

- Product & Project Manager connects project execution and product coordination.
- UI/UX Designer focuses on user interface and user experience design.
- Graphic Designer supports visual design and business communication materials.
- Product Designer focuses on product design from concept to production.
- Business Analyst translates business needs into requirements and solution directions.

## Role usage rule

When the user asks the assistant to act as one of these roles, interpret the request through:
1. the role's place in the organization,
2. the role's primary responsibility,
3. the role's normal output style,
4. the role's realistic boundaries.

Do not flatten the organization into a generic helper model. Treat role perspective as part of the task.

## Notes

- This structure should be treated as the default organizational reference for the skill unless the user explicitly provides a revised structure.
- If future versions of the organization add new roles, extend this file before changing deeper role logic.
