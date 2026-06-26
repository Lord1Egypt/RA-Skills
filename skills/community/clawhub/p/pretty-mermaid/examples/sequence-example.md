sequenceDiagram
    participant U as User
    participant A as API Gateway
    participant B as Backend Service
    participant D as Database
    participant C as Cache
    
    U->>A: POST /api/data
    A->>B: Forward Request
    B->>C: Check Cache
    alt Cache Hit
        C-->>B: Return Cached Data
    else Cache Miss
        B->>D: Query Database
        D-->>B: Return Data
        B->>C: Update Cache
    end
    B-->>A: Return Response
    A-->>U: 200 OK with Data
    
    Note right of U: User makes request
    Note left of D: Database operation
    Note over C: Cache layer