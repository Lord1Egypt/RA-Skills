[Skip to main content](https://java-design-patterns.com/patterns/polling-publisher/#main-content)

# Polling Publisher-Subscriber Pattern in Java: Mastering Asynchronous Messaging Elegantly

ArchitecturalSpring BootKafkaMicroservicesAsynchronous MessagingDecouplingAbout 2 min

* * *

## [Also known as](https://java-design-patterns.com/patterns/polling-publisher/\#also-known-as)

- Event-Driven Architecture
- Asynchronous Pub/Sub Pattern
- Message Queue-Based Polling System

## [Intent of Polling Publisher-Subscriber Pattern](https://java-design-patterns.com/patterns/polling-publisher/\#intent-of-polling-publisher-subscriber-pattern)

The Polling Publisher-Subscriber pattern decouples data producers from consumers by enabling asynchronous, message-driven communication. A service polls a data source and publishes messages to a message broker (e.g., Kafka), which are then consumed by one or more subscriber services.

## [Detailed Explanation of the Pattern with Real-World Examples](https://java-design-patterns.com/patterns/polling-publisher/\#detailed-explanation-of-the-pattern-with-real-world-examples)

### [Real-world analogy](https://java-design-patterns.com/patterns/polling-publisher/\#real-world-analogy)

> A news agency constantly polls for the latest news updates. Once it receives new information, it publishes them to different news outlets (TV, newspapers, apps). Each outlet consumes and displays the updates independently.

### [In plain words](https://java-design-patterns.com/patterns/polling-publisher/\#in-plain-words)

> One service regularly checks for updates (polls) and sends messages to Kafka. Another service listens to Kafka and processes the messages asynchronously.

### [Wikipedia says](https://java-design-patterns.com/patterns/polling-publisher/\#wikipedia-says)

> This pattern closely resembles the [Publish–subscribe model](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern), where messages are sent by publishers and received by subscribers without them knowing each other.

### [Architecture Flow](https://java-design-patterns.com/patterns/polling-publisher/\#architecture-flow)

```
+------------+      +--------+      +-------------+
|  Publisher | ---> | Kafka  | ---> | Subscriber  |
+------------+      +--------+      +-------------+
```

## [Programmatic Example (Spring Boot + Kafka)](https://java-design-patterns.com/patterns/polling-publisher/\#programmatic-example-spring-boot-kafka)

### [Publisher Service](https://java-design-patterns.com/patterns/polling-publisher/\#publisher-service)

- Uses Spring's `@Scheduled` to poll data periodically.
- Publishes data to a Kafka topic.
- Optionally exposes a REST API for manual data publishing.

```java
@Scheduled(fixedRate = 5000)
public void pollAndPublish() {
    String data = pollingService.getLatestData();
    kafkaTemplate.send("updates-topic", data);
}
```

### [Subscriber Service](https://java-design-patterns.com/patterns/polling-publisher/\#subscriber-service)

- Listens to Kafka topic using `@KafkaListener`.
- Processes messages asynchronously.

```java
@KafkaListener(topics = "updates-topic")
public void processUpdate(String message) {
    log.info("Received update: {}", message);
    updateProcessor.handle(message);
}
```

## [When to Use the Polling Publisher-Subscriber Pattern](https://java-design-patterns.com/patterns/polling-publisher/\#when-to-use-the-polling-publisher-subscriber-pattern)

Use this pattern when:

- Real-time push from the producer is not possible.
- Loose coupling between producers and consumers is desired.
- You need asynchronous, scalable event processing.
- You are building an event-driven microservices architecture.

## [Real-World Applications](https://java-design-patterns.com/patterns/polling-publisher/\#real-world-applications)

- Real-time reporting dashboards
- Health check aggregators for distributed systems
- IoT telemetry processing
- Notification and alerting systems

## [Benefits and Trade-offs of Polling Pub/Sub Pattern](https://java-design-patterns.com/patterns/polling-publisher/\#benefits-and-trade-offs-of-polling-pub-sub-pattern)

### [Benefits](https://java-design-patterns.com/patterns/polling-publisher/\#benefits)

- Loose coupling between services
- Asynchronous and scalable architecture
- Fault-tolerant with message persistence in Kafka
- Easy to extend with new consumers or publishers

### [Trade-Offs](https://java-design-patterns.com/patterns/polling-publisher/\#trade-offs)

- Polling introduces latency between data generation and consumption
- Requires managing and configuring Kafka (or other brokers)
- Slightly more complex deployment and infrastructure setup

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/polling-publisher/\#related-java-design-patterns)

- [Observer Pattern](https://java-design-patterns.com/patterns/observer/)
- [Mediator Pattern](https://java-design-patterns.com/patterns/mediator/)
- [Message Queue Pattern](https://java-design-patterns.com/patterns/event-queue/)

## [References and Credits](https://java-design-patterns.com/patterns/polling-publisher/\#references-and-credits)

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spring Kafka Documentation](https://docs.spring.io/spring-kafka)
- [Spring Scheduled Tasks](https://www.baeldung.com/spring-scheduled-tasks)
- [Spring Kafka Tutorial – Baeldung](https://www.baeldung.com/spring-kafka)
- Inspired by: [iluwatar/java-design-patterns](https://github.com/iluwatar/java-design-patterns)