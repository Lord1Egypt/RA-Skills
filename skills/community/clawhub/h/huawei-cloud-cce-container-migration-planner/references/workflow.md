# Workflow

1. Confirm migration goal: same-region, cross-region, multi-cluster, hybrid cloud, version upgrade, or architecture adjustment.
2. Inventory source cluster basics: node pools, addons, network model, and key configurations.
3. Inventory workloads: Deployments, StatefulSets, DaemonSets, Services, Ingresses, PVCs, PVs, ConfigMaps, Secrets.
4. Inventory associated cloud resources: VPC, subnets, security groups, ELB, EIP, EVS, SFS/SFS Turbo.
5. Build dependency matrix: ingress traffic, service dependencies, storage dependencies, configuration dependencies, external systems.
6. Design migration batches with validation points, rollback strategies, and downtime windows.
7. Output the plan — do not execute changes.