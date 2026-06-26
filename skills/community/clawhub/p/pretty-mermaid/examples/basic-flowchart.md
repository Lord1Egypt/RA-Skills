flowchart TD
    Start[Start Process] --> Input{Get Input}
    Input -->|Valid| Process[Process Data]
    Input -->|Invalid| Error[Show Error]
    
    Process --> Validate{Validate Results}
    Validate -->|Success| Output[Output Results]
    Validate -->|Failure| Retry[Retry Process]
    
    Output --> End[End]
    Error --> End
    Retry --> Process
    
    style Start fill:#1a73e8,color:#ffffff,stroke:#0d47a1
    style Input fill:#fbbc04,color:#202124,stroke:#f57c00
    style Process fill:#34a853,color:#ffffff,stroke:#0d652d
    style Validate fill:#ea4335,color:#ffffff,stroke:#b71c1c
    style Output fill:#5f6368,color:#ffffff,stroke:#3c4043
    style Error fill:#ea4335,color:#ffffff,stroke:#b71c1c
    style Retry fill:#fbbc04,color:#202124,stroke:#f57c00
    style End fill:#1a73e8,color:#ffffff,stroke:#0d47a1