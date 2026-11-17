export default {
inject:['service', 'tags'],
data(){return{
    cid:'',
    auth:{dlg:false,pwd:'',visible:false}
}},
created(){
    var c=this.service.curCompany();
    this.cid=c.id;
    this.companyName=c.name;
    if(!this.service.getToken("company",this.cid)) {
        this.auth.dlg=true;
    }
},
methods:{
showOmPg(name) {
    if(!this.service.getToken('backend')){
        this.$refs.errDlg.show(this.tags.noToken);
        return; //还未准备好
    }
    this.service.go_to('/om/'+name);
},
showPage(url) {
    if(!this.service.getToken('backend')){
        this.$refs.errDlg.show(this.tags.noToken);
        return; //还未准备好
    }
    this.service.go_to(url);
},
onAuth() {
    var shaPwd=Secure.sha256(this.auth.pwd);
    var dta={pwd:shaPwd, services:["company","httpdns","backend","bios","appstore"]};
    this.service.request_cloud({method:"POST",url:"/token", data:dta, private:false},"company").then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        for(var i in resp.data) {
            this.service.setToken(i,resp.data[i]);
        }
        this.auth.dlg=false;
        this.service.initServiceList();
    });
}
},

template: `
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
    <q-toolbar>
      <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
    </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list style="min-width: 100px">
 <q-item-label header>{{tags.baseSettings}}</q-item-label>
 <q-item clickable v-close-popup @click="showPage('/cfg')">
   <q-item-section avatar><q-icon color="primary" name="settings"></q-icon></q-item-section>
   <q-item-section no-wrap>{{tags.cfg.title}}</q-item-section>
 </q-item>
 <q-item clickable v-close-popup @click="showPage('/mkt')">
   <q-item-section avatar><q-icon color="primary" name="shop_two"></q-icon></q-item-section>
   <q-item-section no-wrap>{{tags.mkt.title}}</q-item-section>
 </q-item>
 <div v-if="service.mode!='ROOT'">
  <q-separator spaced></q-separator>
  <q-item-label header>{{tags.om.title}}</q-item-label>
  <q-item clickable @click="showOmPg('services')">
   <q-item-section avatar>
    <q-icon color="primary" name="apps"></q-icon>
   </q-item-section>
   <q-item-section>{{tags.om.serviceMng}}</q-item-section>
  </q-item>
  <q-item clickable @click="showOmPg('srvnodes')">
   <q-item-section avatar>
    <q-icon color="primary" name="miscellaneous_services"></q-icon>
   </q-item-section>
   <q-item-section>{{tags.om.srvNodes}}</q-item-section>
  </q-item>
  <q-item clickable @click="showOmPg('dbnodes')">
   <q-item-section avatar>
    <q-icon color="primary" name="storage"></q-icon>
   </q-item-section>
   <q-item-section>{{tags.om.dbNodes}}</q-item-section>
  </q-item>
  <q-item clickable v-ripple @click="showOmPg('execsqls')">
   <q-item-section avatar>
    <q-icon color="primary" name="subscriptions"></q-icon>
   </q-item-section>
   <q-item-section>{{tags.om.execsqls}}</q-item-section>
  </q-item>
  <q-item clickable v-ripple @click="showOmPg('serverlogs')">
   <q-item-section avatar>
    <q-icon color="primary" name="subject"></q-icon>
   </q-item-section>
   <q-item-section>{{tags.om.serverlogs}}</q-item-section>
  </q-item>
 </div>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="auth.dlg" persistent> <!-- admin登录公司获得公司级token -->
  <q-card style="min-width:62vw;max-width:80vw">
    <q-card-section>
      <div class="text-h6">{{tags.cfg.auth}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <div class="col text-subtitle1 ellipsis">{{companyName}} - {{cid}}</div>
     <q-input dense v-model="auth.pwd" autofocus :type="auth.visible?'text':'password'"
      :label="tags.cfg.pwd" @keyup.enter="onAuth">
       <template v-slot:append>
         <q-icon :name="auth.visible ? 'visibility_off':'visibility'"
          class="cursor-pointer" @click="auth.visible=!auth.visible"></q-icon>
       </template>
     </q-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn color="primary" :label="tags.ok" @click="onAuth"></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<component-alert-dialog :title="tags.alert" :errMsgs="tags.errMsgs"
 :close="tags.close" ref="alertDlg"></component-alert-dialog>
`
}