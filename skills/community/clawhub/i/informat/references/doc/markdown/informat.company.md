This document introduces the team in the Informat low-code platform, including team members, team roles, and organizational structure.

## Overview

Informat uses a multi-tenant architecture with three types of users:

- **System Account (Account)**: Created through registration or admin console, serves as login credentials
- **Team Member (CompanyMember)**: Each Account can join multiple teams
- **Application Member (User)**: Each CompanyMember can join multiple applications within a team

A system account cannot perform any operations after login without joining a team. The admin console can disable accounts, force password changes, etc.

## Team Member

A team member (CompanyMember) is the identity of a system account after joining a team. Each team member can have multiple roles and belong to one or more departments.

### How to Join

- Automatically join and get admin role after creating a team
- Accept invitation to join
- Admin adds in console (existing account or create new account)
- Script call `informat.company.addCompanyMember()`

### How to Remove

- Remove via admin console
- User leaves voluntarily
- Script call `informat.company.deleteCompanyMember()`

## Team Roles

Team members are assigned different team roles, which are associated with corresponding permissions. Team members can have multiple roles.

### Default Roles

- **Admin**: Has all permissions, can design applications
- **Member**: Only has permission to use applications

### Role Permission List

| Permission ID | Permission Name | Description |
|--------------|----------------|-------------|
| CompanySetting | Team Settings | Manage team basic info and configuration |
| InviteMember | Member Management | Invite, add, remove team members |
| CompanyApp | Application Management | Create, edit, delete applications |
| CompanyAppDesigner | Application Design | Design application data tables, workflows, dashboards, etc. |
| CompanyAppMonitor | Application Monitoring | Monitor application running status |

When creating or editing a role, set the role's permissions via the `permissionIds` field, using the permission IDs from the table above.

## Organization Structure (Department)

Each team can build a department organizational tree with parent-child relationships. Each department can have one or more CompanyMembers as managers.

Every team member must join at least one department. The member's department list is recorded in the `departmentList` field.

### How to Create

- Automatically created after team deployment
- Admin creates manually
- Script call `informat.dept.addDept()`

### How to Delete

- Admin deletes
- Script call `informat.dept.deleteDept()`

## Application Member

After a team member joins an application, they become an application member (User) and are assigned different application roles. Each application has a default "Admin" role with all permissions.

### How to Join

- Application admin adds user
- Application admin sets authorization method to "by role and department"
- Script call `informat.user.addUser()`

### How to Remove

- Application admin removes
- If authorization is "by role and department", automatically removed when user's role or department is no longer in the authorized scope
- Script call `informat.user.deleteUser()`
