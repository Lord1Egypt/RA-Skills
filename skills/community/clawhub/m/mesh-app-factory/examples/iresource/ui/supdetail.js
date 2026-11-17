const EMPTY_CONTACT={name:'',sex:'',post:'',phone:'',cmt:''};
export default {
inject:['service', 'tags'],
data() {return {
    id:this.$route.query.id,
    supInfo:{}, //供应商信息
    contacts:[], //供应商联系人
    ctrl:{fun:'',dta:{}},
    edtContact:{show:false,no:-2,dta:{}}
}},
created(){
    this.get();
    this.getContacts();
},
methods:{
get() {
    var url = "/api/supplier/get?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        dt.setTime(resp.data.createAt*60000);
        resp.data.createAt_s=date2str(dt);
        this.supInfo=resp.data;
    })
},
remove() {
    var opts={method:"DELETE",url:"/supplier/remove?id="+this.id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.service.back();
    });
},
update() {
    var opts={method:"PUT",url:"/supplier/update",data:this.ctrl.dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        copyObjTo(this.ctrl.dta, this.supInfo);
        this.ctrl.fun='';
    });
},
show_edit() {
    copyObjTo(this.supInfo, this.ctrl.dta);
    this.ctrl.dta.id=this.id;
    this.ctrl.fun='edit';
},
//联系人
getContacts() {
    var url = "/api/contact/list?supplier="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        for(var e of resp.data.list) {
            dt.setTime(e.createAt*60000);
            e.createAt_s=date2str(dt);
            e.sex_s=this.tags.sex[e.sex];
        }
        this.contacts=resp.data.list;
    });
},
show_contact(no) {
    if(no>-1) {
        copyObjTo(this.contacts[no], this.edtContact.dta);
        this.edtContact.id=this.contacts[no].id;
    } else {
        copyObjTo(EMPTY_CONTACT, this.edtContact.dta);
    }
    this.edtContact.no=no;
    this.edtContact.show=true;
},
contact_do() {
    var opts;
    if(this.edtContact.no>-1) {
        opts={method:"PUT",url:"/contact/update",data:this.edtContact.dta};
    } else {
        var dta=cloneObj(this.edtContact.dta);
        dta.supplier=this.id;
        opts={method:"POST",url:"/contact/add",data:dta};
    }
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        if(this.edtContact.no>-1) {
            copyObjTo(this.edtContact.dta, this.contacts[this.edtContact.no]);
        } else {
            var sex=this.tags.sex[this.edtContact.dta.sex];
            var o = {id:resp.data.id, createAt_s:date2str(new Date()), sex_s:sex};
            copyObjTo(this.edtContact.dta, o);
            this.contacts.push(o);
        }
        this.edtContact.no=-2;
        this.edtContact.show=false;
    });
},
rmv_contact(i) {
    var url = "/api/contact/remove?id="+this.contacts[i].id;
    request({method:"DELETE",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.contacts.splice(i,1);
        this.edtContact.show=false;
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.detail}}-{{supInfo.name}}</q-toolbar-title>
    <q-btn icon="delete_forever" @click="remove" flat dense></q-btn>
    <q-btn icon="edit" @click="show_edit" flat dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div v-if="ctrl.fun==''">
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.name}}</q-item-section>
   <q-item-section>{{supInfo.name}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.supplier.taxid}}</q-item-section>
   <q-item-section>{{supInfo.taxid}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.supplier.addr}}</q-item-section>
   <q-item-section>{{supInfo.addr}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.supplier.business}}</q-item-section>
   <q-item-section>{{supInfo.business}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section>{{supInfo.cmt}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.createAt}}</q-item-section>
   <q-item-section>{{supInfo.createAt_s}}</q-item-section>
  </q-item>
 </q-list>
</div>
<div v-else>
 <q-list dense>
 <q-item>
  <q-item-section>{{tags.name}}</q-item-section>
  <q-item-section><q-input v-model="ctrl.dta.name" dense></q-input></q-item-section>
 </q-item>
 <q-item>
  <q-item-section>{{tags.supplier.taxid}}</q-item-section>
  <q-item-section><q-input v-model="ctrl.dta.taxid" dense></q-input></q-item-section>
 </q-item>
 <q-item>
  <q-item-section>{{tags.supplier.addr}}</q-item-section>
  <q-item-section><q-input v-model="ctrl.dta.addr" dense></q-input></q-item-section>
 </q-item>
 <q-item>
  <q-item-section>{{tags.supplier.business}}</q-item-section>
  <q-item-section><q-input v-model="ctrl.dta.business" dense></q-input></q-item-section>
 </q-item>
 <q-item>
  <q-item-section>{{tags.cmt}}</q-item-section>
  <q-item-section><q-input v-model="ctrl.dta.cmt" dense></q-input></q-item-section>
 </q-item>
 <q-item>
  <q-item-section>{{tags.createAt}}</q-item-section>
  <q-item-section>{{supInfo.createAt_s}}</q-item-section>
 </q-item>
 </q-list>
 <div class="text-right">
  <q-btn flat :label="tags.cancel" color="primary" @click="ctrl.fun=''"></q-btn>
  <q-btn icon="done" :label="tags.ok" color="primary" @click="update"></q-btn>
 </div>
</div>
<q-separator inset></q-separator>
<q-banner inline-actions class="bg-indigo-1 q-ma-sm" dense>
  {{tags.contact.title}}
  <template v-slot:action>
   <q-icon flat color="primary" name="add_circle" @click.stop="show_contact(-2)"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item v-for="(c,i) in contacts" clickable @click=show_contact(i)>
   <q-item-section>
    <q-item-label>{{c.name}}({{c.sex_s}})</q-item-label>
    <q-item-label caption>{{c.post}}</q-item-label>
   </q-item-section>
   <q-item-section>{{c.phone}}</q-item-section>
   <q-item-section>
    <q-item-label>{{c.cmt}}</q-item-label>
    <q-item-label caption>{{c.creator}}</q-item-label>
   </q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="edtContact.show">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.contact.title}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.contact.name" v-model="edtContact.dta.name" dense></q-input>
   <div class="q-gutter-sm">
     <q-radio v-model="edtContact.dta.sex" val="F" :label="tags.sex.F"></q-radio>
     <q-radio v-model="edtContact.dta.sex" val="M" :label="tags.sex.M"></q-radio>
     <q-radio v-model="edtContact.dta.sex" val="U" :label="tags.sex.U"></q-radio>
   </div>
   <q-input :label="tags.contact.post" v-model="edtContact.dta.post" dense></q-input>
   <q-input :label="tags.contact.phone" v-model="edtContact.dta.phone" dense></q-input>
   <q-input :label="tags.cmt" v-model="edtContact.dta.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn flat :label="tags.remove" color="red" @click="rmv_contact(edtContact.no)" flat v-show="edtContact.no>-1"></q-btn>
   <q-btn :label="tags.ok" color="primary" @click="contact_do"></q-btn>
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}