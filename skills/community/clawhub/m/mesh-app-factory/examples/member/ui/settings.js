export default {
inject:['service', 'tags'],
data() {return {
    tab:'package',
    segTypes:[],
    pkgUnits:[],
    template:{},
    packages:[],
    newSeg:{k:'',n:'',t:'s'},
    newPackage:{name:'',cls:'0',price:'',val:'',ext:{}},
    dlg:{pkg:false,seg:false}
}},
created(){
    for(var n in this.tags.segTypes){
        this.segTypes.push({value:n,label:this.tags.segTypes[n]})
    }
    for(var n in this.tags.pkgUnits){
        this.pkgUnits.push({value:n,label:this.tags.pkgUnits[n]})
    }
   
    this.query_pkgs();
    this.query_tmpls();
},

methods:{
query_tmpls() {
    var url="/api/template/get?unuseCache=1";
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            Console.debug("Url:" + url + ",code:" + resp.code + ",info:" + resp.info);
            return;
        }
        if(resp.data.template) {
            this.template=resp.data.template;
        }
    });
},
query_pkgs() {
    var url="/api/package/list?unuseCache=1";
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            Console.debug("Url:" + url + ",code:" + resp.code + ",info:" + resp.info);
            return;
        }
        this.packages=resp.data.packages; //id,createAt,name,cls,val,price,ext
    });
},
rmv_tpl_seg(n){
    var tpls={};
    for(var k in this.template) {
        if(k!=n) {
            tpls[k]=this.template[k];
        }
    }
    this.template=tpls;
    this.save_tpl();
},
add_tpl_seg(){
    this.template[this.newSeg.k]={n:this.newSeg.n,t:this.newSeg.t};
    this.save_tpl();
},
save_tpl(){
    var url="/api/template/set";
    var req={template:this.template};
    request({method:"PUT",url:url,data:req}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.newSeg={k:'',n:'',t:'s'};
        this.dlg.seg=false;
    });
},
rmv_package(id,n){
    var url="/api/package/remove?id="+id;
    request({method:"DELETE",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.packages.splice(n,1);
    });
},
add_package(){
    var opts={method:"POST",url:"/api/package/set", data:this.newPackage}
    request(opts, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query_pkgs();
        this.newPackage={name:'',cls:'0',price:'',val:'',ext:{}};
        this.dlg.pkg=false;
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary" elevated>
   <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{tags.settings}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">

<q-tabs v-model="tab" class="text-primary">
  <q-tab name="package" icon="business_center" :label="tags.package"></q-tab>
  <q-tab name="template" icon="perm_contact_calendar" :label="tags.template"></q-tab>
</q-tabs>
<q-separator></q-separator>
<q-tab-panels v-model="tab" animated swipeable transition-prev="jump-up" transition-next="jump-up">
  <q-tab-panel name="template">
   <q-list>
    <q-item>
     <q-item-section><q-item-label caption>{{tags.segName}}</q-item-label></q-item-section>
     <q-item-section avatar><q-icon name="add_circle" color="primary" @click="dlg.seg=true"></q-icon></q-item-section>
    </q-item>
    <q-separator></q-separator>
    <q-item v-for="(tpl,k) in template">
     <q-item-section>
      <q-item-label>{{tpl.n}}</q-item-label>
      <q-item-label caption>{{tags.segKey}}:{{k}}, {{tags.segType}}:{{tags.segTypes[tpl.t]}}</q-item-label>
     </q-item-section>
     <q-item-section avatar><q-icon name="cancel" color="green" @click="rmv_tpl_seg(k)"></q-icon></q-item-section>
    </q-item>
   </q-list>
  </q-tab-panel>
  <q-tab-panel name="package">
    <q-card class="my-card">
    <q-card-section>
     {{tags.pkgAlert1}}
    </q-card-section>
    <q-card-section>
     {{tags.pkgAlert2}}
    </q-card-section>
   </q-card>
   <q-list>
    <q-item>
     <q-item-section><q-item-label caption>{{tags.pkgName}}</q-item-label></q-item-section>
     <q-item-section avatar><q-icon color="primary" name="add_circle" @click="dlg.pkg=true"></q-icon></q-item-section>
    </q-item>
    <q-separator></q-separator>
    <q-item v-for="(p,n) in packages">
     <q-item-section>
      <q-item-label>{{p.name}}</q-item-label>
      <q-item-label caption>{{tags.pkgPrice}}:{{p.price}}, {{tags.pkgVal}}:{{p.val}}{{tags.pkgUnits[p.cls]}}</q-item-label>
     </q-item-section>
     <q-item-section avatar><q-icon color="green" name="cancel" @click="rmv_package(p.id,n)"></q-icon></q-item-section>
    </q-item>
   </q-list>
  </q-tab-panel>
</q-tab-panels>

    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="dlg.pkg">
  <q-card style="min-width:70vw" class="q-pa-md">
    <q-card-section>
      <div class="text-h6">{{tags.newPkg}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <q-input v-model="newPackage.name" :label="tags.pkgName"></q-input>
      <q-input v-model="newPackage.price" :label="tags.pkgPrice"></q-input>
      <div class="q-gutter-md row">
       <div class="col"><q-input v-model="newPackage.val" :label="tags.pkgVal"></q-input></div>
       <div class="col"><q-select v-model="newPackage.cls" :options="pkgUnits" emit-value map-options></q-select></div>
      </div>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
      <q-btn :label="tags.ok" color="primary" @click="add_package"></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<q-dialog v-model="dlg.seg">
  <q-card style="min-width:70vw" class="q-pa-md">
    <q-card-section>
      <div class="text-h6">{{tags.newSeg}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <q-input v-model="newSeg.n" :label="tags.segName"></q-input>
      <q-input v-model="newSeg.k" :label="tags.segKey" :hint="tags.segKeyHint" hide-hint></q-input>
      <q-select v-model="newSeg.t" :options="segTypes" emit-value map-options></q-select>
    </q-item>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
      <q-btn :label="tags.ok" color="primary" @click="add_tpl_seg"></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}
