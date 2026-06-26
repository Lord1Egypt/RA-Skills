# Outline API Endpoints Reference

All endpoints are POST. Required params marked with *.


## Attachments

**/attachments.create** — Create an attachment
  Params: name(string) *, documentId(string), contentType(string) *, size(number) *
  Required: name, contentType, size

**/attachments.redirect** — Retrieve an attachment
  Params: id(string) *
  Required: id

**/attachments.delete** — Delete an attachment
  Params: id(string) *
  Required: id


## Auth

**/auth.info** — Retrieve auth

**/auth.config** — Retrieve auth config


## Collections

**/collections.info** — Retrieve a collection
  Params: id(string) *
  Required: id

**/collections.documents** — Retrieve a collections document structure
  Params: id(string) *
  Required: id

**/collections.list** — List all collections
  Params: query(string), statusFilter(array)

**/collections.create** — Create a collection
  Params: name(string) *, description(string), permission(#/components/schemas/Permission), icon(string), color(string), sharing(boolean)
  Required: name

**/collections.update** — Update a collection
  Params: id(string) *, name(string), description(string), permission(#/components/schemas/Permission), icon(string), color(string), sharing(boolean)
  Required: id

**/collections.add_user** — Add a collection user
  Params: id(string) *, userId(string) *, permission(#/components/schemas/Permission)
  Required: id, userId

**/collections.remove_user** — Remove a collection user
  Params: id(string) *, userId(string) *
  Required: id, userId

**/collections.memberships** — List all collection memberships
  Params: id(string) *, query(string), permission(#/components/schemas/Permission)
  Required: id

**/collections.add_group** — Add a group to a collection
  Params: id(string) *, groupId(string) *, permission(#/components/schemas/Permission)
  Required: id, groupId

**/collections.remove_group** — Remove a collection group
  Params: id(string) *, groupId(string) *
  Required: id, groupId

**/collections.group_memberships** — List all collection group members
  Params: id(string) *, query(string), permission(#/components/schemas/Permission)
  Required: id

**/collections.delete** — Delete a collection
  Params: id(string) *
  Required: id

**/collections.export** — Export a collection
  Params: format(string), id(string) *
  Required: id

**/collections.export_all** — Export all collections
  Params: format(string), includeAttachments(boolean), includePrivate(boolean)


## Comments

**/comments.create** — Create a comment
  Params: id(string), documentId(string) *, parentCommentId(string), data(object), text(string)
  Required: documentId

**/comments.info** — Retrieve a comment
  Params: id(string) *, includeAnchorText(boolean)
  Required: id

**/comments.update** — Update a comment
  Params: id(string) *, data(object) *
  Required: id, data

**/comments.delete** — Delete a comment
  Params: id(string) *
  Required: id

**/comments.list** — List all comments
  Params: documentId(string), collectionId(string), includeAnchorText(boolean)


## Dataattributes

**/dataAttributes.info** — Retrieve a data attribute
  Params: id(string) *
  Required: id

**/dataAttributes.list** — List all data attributes

**/dataAttributes.create** — Create a data attribute
  Params: name(string) *, description(string), dataType(#/components/schemas/DataAttributeDataType) *, options(#/components/schemas/DataAttributeOptions), pinned(boolean)
  Required: name, dataType

**/dataAttributes.update** — Update a data attribute
  Params: id(string) *, name(string) *, description(string), options(#/components/schemas/DataAttributeOptions), pinned(boolean)
  Required: id, name

**/dataAttributes.delete** — Delete a data attribute
  Params: id(string) *
  Required: id


## Documents

**/documents.info** — Retrieve a document
  Params: id(string), shareId(string)

**/documents.import** — Import a file as a document

**/documents.export** — Export a document.
  Params: id(string) *, paperSize(string), signedUrls(number), includeChildDocuments(boolean)
  Required: id

**/documents.list** — List all documents
  Params: collectionId(string), userId(string), backlinkDocumentId(string), parentDocumentId(string), statusFilter(array)

**/documents.documents** — Retrieve a document's child structure
  Params: id(string) *
  Required: id

**/documents.drafts** — List all draft documents
  Params: collectionId(string), dateFilter(string)

**/documents.viewed** — List all recently viewed documents

**/documents.answerQuestion** — Query documents with natural language
  Params: query(string), userId(string), collectionId(string), documentId(string), statusFilter(string), dateFilter(string)

**/documents.search_titles** — Search document titles
  Params: query(string) *, collectionId(string), userId(string), documentId(string), statusFilter(array), dateFilter(string), shareId(string), sort(string), direction(string)
  Required: query

**/documents.search** — Search all documents
  Params: query(string), userId(string), collectionId(string), documentId(string), statusFilter(array), dateFilter(string), shareId(string), snippetMinWords(number), snippetMaxWords(number), sort(string), direction(string)

**/documents.create** — Create a document
  Params: id(string), title(string), text(string), icon(string), color(string), collectionId(string), parentDocumentId(string), templateId(string), publish(boolean), fullWidth(boolean), createdAt(string), dataAttributes(array)

**/documents.update** — Update a document
  Params: id(string) *, title(string), text(string), icon(string), color(string), fullWidth(boolean), templateId(string), collectionId(string), insightsEnabled(boolean), editMode(#/components/schemas/TextEditMode), publish(boolean), dataAttributes(array)
  Required: id

**/documents.templatize** — Create a template from a document
  Params: id(string) *, collectionId(string), publish(boolean) *
  Required: id, publish

**/documents.unpublish** — Unpublish a document
  Params: id(string) *, detach(boolean)
  Required: id

**/documents.move** — Move a document
  Params: id(string) *, collectionId(string), parentDocumentId(string), index(number)
  Required: id

**/documents.archive** — Archive a document
  Params: id(string) *
  Required: id

**/documents.restore** — Restore a document
  Params: id(string) *, collectionId(string), revisionId(string)
  Required: id

**/documents.delete** — Delete a document
  Params: id(string) *, permanent(boolean)
  Required: id

**/documents.users** — List document users
  Params: id(string) *, query(string), userId(string)
  Required: id

**/documents.memberships** — List document memberships
  Params: id(string) *, query(string), permission(#/components/schemas/Permission)
  Required: id

**/documents.add_user** — Add a document user
  Params: id(string) *, userId(string) *, permission(#/components/schemas/Permission)
  Required: id, userId

**/documents.remove_user** — Remove a document user
  Params: id(string) *, userId(string) *
  Required: id, userId

**/documents.archived** — List all archived documents
  Params: collectionId(string)

**/documents.deleted** — List all deleted documents

**/documents.duplicate** — Duplicate a document
  Params: id(string) *, title(string), recursive(boolean), publish(boolean), collectionId(string), parentDocumentId(string)
  Required: id

**/documents.add_group** — Add a group to a document
  Params: id(string) *, groupId(string) *, permission(#/components/schemas/Permission)
  Required: id, groupId

**/documents.remove_group** — Remove a group from a document
  Params: id(string) *, groupId(string) *
  Required: id, groupId

**/documents.group_memberships** — List document group memberships
  Params: id(string) *, query(string), permission(#/components/schemas/Permission)
  Required: id

**/documents.empty_trash** — Empty trash


## Events

**/events.list** — List all events
  Params: name(string), actorId(string), documentId(string), collectionId(string), auditLog(boolean)


## Fileoperations

**/fileOperations.info** — Retrieve a file operation
  Params: id(string) *
  Required: id

**/fileOperations.delete** — Delete a file operation
  Params: id(string) *
  Required: id

**/fileOperations.redirect** — Retrieve the file
  Params: id(string) *
  Required: id

**/fileOperations.list** — List all file operations
  Params: type(string) *
  Required: type


## Groups

**/groups.info** — Retrieve a group
  Params: id(string) *
  Required: id

**/groups.list** — List all groups
  Params: userId(string), externalId(string), query(string)

**/groups.create** — Create a group
  Params: name(string) *
  Required: name

**/groups.update** — Update a group
  Params: id(string) *, name(string) *
  Required: id, name

**/groups.delete** — Delete a group
  Params: id(string) *
  Required: id

**/groups.memberships** — List all group members
  Params: id(string) *, query(string)
  Required: id

**/groups.add_user** — Add a group member
  Params: id(string) *, userId(string) *
  Required: id, userId

**/groups.remove_user** — Remove a group member
  Params: id(string) *, userId(string) *
  Required: id, userId


## Oauthauthentications

**/oauthAuthentications.list** — List accessible OAuth authentications

**/oauthAuthentications.delete** — Delete an OAuth authentiation
  Params: oauthClientId(string) *, scope(array)
  Required: oauthClientId


## Oauthclients

**/oauthClients.info** — Retrieve an OAuth client
  Params: id(string), clientId(string)

**/oauthClients.list** — List accessible OAuth clients

**/oauthClients.create** — Create an OAuth client
  Params: name(string) *, description(string), developerName(string), developerUrl(string), avatarUrl(string), redirectUris(array) *, published(boolean)
  Required: name, redirectUris

**/oauthClients.update** — Update an OAuth client
  Params: id(string) *, name(string), description(string), developerName(string), developerUrl(string), avatarUrl(string), redirectUris(array), published(boolean)
  Required: id

**/oauthClients.rotate_secret** — Rotate the secret for an OAuth client
  Params: id(string) *
  Required: id

**/oauthClients.delete** — Delete an OAuth client
  Params: id(string) *
  Required: id


## Revisions

**/revisions.info** — Retrieve a revision
  Params: id(string) *
  Required: id

**/revisions.list** — List all revisions
  Params: documentId(string)


## Shares

**/shares.info** — Retrieve a share object
  Params: id(string), documentId(string)

**/shares.list** — List all shares
  Params: query(string)

**/shares.create** — Create a share
  Params: documentId(string) *
  Required: documentId

**/shares.update** — Update a share
  Params: id(string) *, published(boolean) *
  Required: id, published

**/shares.revoke** — Revoke a share
  Params: id(string) *
  Required: id


## Stars

**/stars.create** — Create a star
  Params: documentId(string), collectionId(string), index(string)

**/stars.list** — List all stars

**/stars.update** — Update a stars order in the sidebar
  Params: id(string) *, index(string) *
  Required: id, index

**/stars.delete** — Delete a star
  Params: id(string) *
  Required: id


## Templates

**/templates.create** — Create a template
  Params: id(string), title(string) *, data(object) *, icon(string), color(string), collectionId(string)
  Required: title, data

**/templates.list** — List all templates
  Params: collectionId(string)

**/templates.info** — Retrieve a template
  Params: id(string) *
  Required: id

**/templates.update** — Update a template
  Params: id(string) *, title(string), data(object), icon(string), color(string), fullWidth(boolean), collectionId(string)
  Required: id

**/templates.delete** — Delete a template
  Params: id(string) *
  Required: id

**/templates.restore** — Restore a template
  Params: id(string) *
  Required: id

**/templates.duplicate** — Duplicate a template
  Params: id(string) *, title(string), collectionId(string)
  Required: id


## Users

**/users.invite** — Invite users
  Params: invites(array) *
  Required: invites

**/users.info** — Retrieve a user
  Params: id(string) *
  Required: id

**/users.list** — List all users
  Params: query(string), emails(array), filter(string), role(#/components/schemas/UserRole)

**/users.update** — Update a user
  Params: name(string), language(string), avatarUrl(string)

**/users.update_role** — Change a users role
  Params: id(string) *, role(#/components/schemas/UserRole) *
  Required: id, role

**/users.suspend** — Suspend a user
  Params: id(string) *
  Required: id

**/users.activate** — Activate a user
  Params: id(string) *
  Required: id

**/users.delete** — Delete a user
  Params: id(string) *
  Required: id


## Views

**/views.list** — List all views
  Params: documentId(string) *, includeSuspended(boolean)
  Required: documentId

**/views.create** — Create a view
  Params: documentId(string) *
  Required: documentId
