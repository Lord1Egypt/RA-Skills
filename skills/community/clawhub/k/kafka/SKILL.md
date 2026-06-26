---
name: kafka
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [kafka, tool, utility]
description: "Produce, consume, and manage Kafka topics with lag monitoring and data export. Use when publishing messages, consuming topics, monitoring consumer lag."
---

# kafka

Produce, consume, and manage Kafka topics with lag monitoring and data export. Use when publishing messages, consuming topics, monitoring consumer lag.

## Commands

### `KAFKA_BOOTSTRAP`

Bootstrap servers (default: localhost:9092)

```bash
scripts/script.sh KAFKA_BOOTSTRAP
```

### `KAFKA_ZOOKEEPER`

Zookeeper address (default: localhost:2181)

```bash
scripts/script.sh KAFKA_ZOOKEEPER
```

### `KAFKA_HOME`

Kafka installation directory

```bash
scripts/script.sh KAFKA_HOME
```

### `topics`

List all topics with partition counts

```bash
scripts/script.sh topics
```

### `create-topic`

Create topic (partitions, replication factor)

```bash
scripts/script.sh create-topic <name> [p] [r]
```

### `describe`

Detailed topic description

```bash
scripts/script.sh describe <topic>
```

### `produce`

Produce a message (optional key)

```bash
scripts/script.sh produce <topic> <msg> [key]
```

### `consume`

Consume messages (default: 10, from-beginning)

```bash
scripts/script.sh consume <topic> [count] [from]
```

### `groups`

List all consumer groups

```bash
scripts/script.sh groups
```

### `lag`

Show consumer group lag

```bash
scripts/script.sh lag <group>
```

### `config`

Show connection config and available tools

```bash
scripts/script.sh config
```

### `status`

Cluster health and status check

```bash
scripts/script.sh status
```

### `delete-topic`

Delete a topic (with confirmation)

```bash
scripts/script.sh delete-topic <topic>
```

### `partitions`

Increase topic partitions

```bash
scripts/script.sh partitions <topic> <count>
```

### `offsets`

Show earliest/latest offsets

```bash
scripts/script.sh offsets <topic>
```

## Requirements

- Kafka CLI tools

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
